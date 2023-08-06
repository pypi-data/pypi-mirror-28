# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

import re
import cgi
import time
import functools
import logging
import json

from datetime import datetime

from itsdangerous import SignatureExpired, BadSignature

from jose import jwt

from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from werkzeug.http import dump_cookie
from werkzeug.wsgi import get_current_url
from werkzeug.utils import redirect
from werkzeug.routing import Rule
from werkzeug.wrappers import Response
from werkzeug.exceptions import BadRequest, Forbidden, NotFound

from isso.compat import text_type as str

from isso import utils, local
from isso.utils import http, parse, JSONResponse as JSON
from isso.views import requires
from isso.utils.hash import sha1

logger = logging.getLogger("isso")

# from Django appearently, looks good to me *duck*
__url_re = re.compile(
    r'^'
    r'(https?://)?'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)'
    r'$', re.IGNORECASE)


def isurl(text):
    return __url_re.match(text) is not None


def normalize(url):
    if not url.startswith(("http://", "https://")):
        return "http://" + url
    return url


def xhr(func):
    """A decorator to check for CSRF on POST/PUT/DELETE using a <form>
    element and JS to execute automatically (see #40 for a proof-of-concept).

    When an attacker uses a <form> to downvote a comment, the browser *should*
    add a `Content-Type: ...` header with three possible values:

    * application/x-www-form-urlencoded
    * multipart/form-data
    * text/plain

    If the header is not sent or requests `application/json`, the request is
    not forged (XHR is restricted by CORS separately).
    """

    def dec(self, env, req, *args, **kwargs):

        if req.content_type and not req.content_type.startswith("application/json"):
            raise Forbidden("CSRF")
        return func(self, env, req, *args, **kwargs)

    return dec


class API(object):

    FIELDS = set(['id', 'parent', 'text', 'auth_method', 'auth_id', 'author', 'website',
                  'pictureURL', 'mode', 'created', 'modified', 'likes', 'dislikes', 'hash',
                  'role_name', 'role_string'])

    # comment fields, that can be submitted
    ACCEPT = set(['text', 'author', 'website', 'email', 'parent', 'title',
                  'auth_method', 'auth_id', 'id_token', 'pictureURL'])

    VIEWS = [
        ('fetch',   ('GET', '/')),
        ('new',     ('POST', '/new')),
        ('count',   ('GET', '/count')),
        ('counts',  ('POST', '/count')),
        ('view',    ('GET', '/id/<int:id>')),
        ('edit',    ('PUT', '/id/<int:id>')),
        ('delete',  ('DELETE', '/id/<int:id>')),
        ('moderate',('GET',  '/id/<int:id>/<any(activate,delete):action>/<string:key>')),
        ('moderate',('POST', '/id/<int:id>/<any(activate,delete):action>/<string:key>')),
        ('like',    ('POST', '/id/<int:id>/like')),
        ('dislike', ('POST', '/id/<int:id>/dislike')),
        ('demo',    ('GET', '/demo')),
        ('preview', ('POST', '/preview'))
    ]

    GOOGLE_ISSUERS = ["accounts.google.com", "https://accounts.google.com"]
    GOOGLE_CERT_URL = "https://www.googleapis.com/oauth2/v1/certs"
    FACEBOOK_GRAPH_HOST = "https://graph.facebook.com"

    google_certs = None

    def __init__(self, isso, hasher):

        self.isso = isso
        API.isso = isso
        self.hash = hasher.uhash
        self.cache = isso.cache
        self.signal = isso.signal

        self.conf = isso.conf.section("general")
        self.openid_conf = isso.conf.section("openid")
        self.facebook_conf = isso.conf.section("facebook")
        self.google_conf = isso.conf.section("google")
        self.moderated = isso.conf.getboolean("moderation", "enabled")
        self.parse_users(isso.conf)

        if isso.conf.get("gui", "max-comments-top") == "inf":
            self.max_comments_top = None
        else:
            self.max_comments_top = isso.conf.getint("gui", "max-comments-top")
        if isso.conf.get("gui", "max-comments-nested") == "inf":
            self.max_comments_nested = None
        else:
            self.max_comments_nested = isso.conf.getint("gui", "max-comments-nested")

        # These configuration records can be read out by client
        self.public_conf = {}
        self.public_conf["max-age"] = isso.conf.getint("general", "max-age")
        self.public_conf["allow-unauthorized"] = isso.conf.getboolean("general", "allow-unauthorized")
        self.public_conf["reply-to-self"] = isso.conf.getboolean("guard", "reply-to-self")
        self.public_conf["require-email"] = isso.conf.getboolean("guard", "require-email")
        self.public_conf["css"] = isso.conf.getboolean("gui", "css")
        self.public_conf["lang"] = isso.conf.get("gui", "lang")
        self.public_conf["max-comments-top"] = isso.conf.get("gui", "max-comments-top")
        self.public_conf["max-comments-nested"] = isso.conf.get("gui", "max-comments-nested")
        self.public_conf["reveal-on-click"] = isso.conf.getint("gui", "reveal-on-click")
        self.public_conf["avatar"] = isso.conf.getboolean("avatar", "enabled")
        self.public_conf["avatar-bg"] = isso.conf.get("avatar", "background")
        self.public_conf["avatar-fg"] = isso.conf.get("avatar", "foreground")
        self.public_conf["vote"] = isso.conf.getboolean("vote", "enabled")
        self.public_conf["vote-levels"] = isso.conf.get("vote", "levels")
        self.public_conf["openid-enabled"] = isso.conf.getboolean("openid", "enabled")
        self.public_conf["facebook-enabled"] = isso.conf.getboolean("facebook", "enabled")
        self.public_conf["facebook-app-id"] = isso.conf.get("facebook", "app-id")
        self.public_conf["google-enabled"] = isso.conf.getboolean("google", "enabled")
        self.public_conf["google-client-id"] = isso.conf.get("google", "client-id")

        self.guard = isso.db.guard
        self.threads = isso.db.threads
        self.comments = isso.db.comments

        for (view, (method, path)) in self.VIEWS:
            isso.urls.add(
                Rule(path, methods=[method], endpoint=getattr(self, view)))

    @classmethod
    def update_google_certs(cls):
        if API.google_certs:
            for key in API.google_certs:
                if datetime.utcnow() <= API.google_certs[key].not_valid_after:
                    return
        with http.curl('GET', API.GOOGLE_CERT_URL, timeout=5) as resp:
            try:
                assert resp and resp.getcode() == 200
                pems = json.loads(resp.read())
                API.google_certs = {key: load_pem_x509_certificate(pems[key].encode("ascii"), default_backend()) for key in pems}
            except (AssertionError, ValueError):
                logger.warn("failed to renew Google certificates")

    @classmethod
    def validate_jwt(cls, token, certificates, audience, issuers):
        for cert in certificates.values():
            pubkey = cert.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
            for iss in issuers:
                try:
                    return jwt.decode(token, pubkey, audience=audience, issuer=iss, options={'verify_at_hash': False})
                except:
                    pass
        return False

    def validate_fb_token(self, token, uid):
        appid = self.facebook_conf.get("app-id")
        req_url = "%s/debug_token?input_token=%s&access_token=%s|%s" % (API.FACEBOOK_GRAPH_HOST, token, appid,
                                                                        self.facebook_conf.get("app-secret"))
        with http.curl('GET', req_url, timeout=5) as resp:
            try:
                assert resp and resp.getcode() == 200
                data = json.loads(resp.read())["data"]
                assert data["is_valid"]
                assert data["user_id"] == uid
                assert data["app_id"] == appid
                assert datetime.utcnow() <= datetime.utcfromtimestamp(data["expires_at"])
                return True
            except (AssertionError, ValueError, KeyError):
                return False

    def verify(self, comment):

        if "text" not in comment:
            return False, "text is missing"

        if not isinstance(comment.get("parent"), (int, type(None))):
            return False, "parent must be an integer or null"

        for key in ("text", "author", "website", "email"):
            if not isinstance(comment.get(key), (str, type(None))):
                return False, "%s must be a string or null" % key

        if len(comment["text"].rstrip()) < 3:
            return False, "text is too short (minimum length: 3)"

        if len(comment["text"]) > 65535:
            return False, "text is too long (maximum length: 65535)"

        if len(comment.get("email") or "") > 254:
            return False, "http://tools.ietf.org/html/rfc5321#section-4.5.3"

        if comment.get("website"):
            if len(comment["website"]) > 254:
                return False, "arbitrary length limit"
            if not isurl(comment["website"]):
                return False, "Website not Django-conform"

        return True, ""

    def authenticate(self, comment):

        if ("auth_method" not in comment or comment["auth_method"] is None) and self.conf.getboolean("allow-unauthorized"):
            pass
        elif comment["auth_method"] == "openid" and self.openid_conf.getboolean("enabled"):
            idPattern = re.compile("^[0-9a-zA-Z]+$")
            if "id_token" not in comment or not idPattern.match(comment["id_token"]):
                return False, "invalid session ID"
            session = self.isso.db.openid_sessions.get(comment["id_token"])
            if session is None or not session["authorized"]:
                return False, "unknown or expired session ID"
        elif comment["auth_method"] == "facebook" and self.facebook_conf.getboolean("enabled"):
            idPattern = re.compile("^[0-9]+$")
            if "auth_id" not in comment or not idPattern.match(comment["auth_id"]):
                return False, "invalid Facebook UID"
            if "id_token" not in comment:
                return False, "Facebook token missing"
            if not self.validate_fb_token(comment["id_token"], comment["auth_id"]):
                return False, "Facebook token validation failed"
        elif comment["auth_method"] == "google" and self.google_conf.getboolean("enabled"):
            idPattern = re.compile("^[0-9]+$")
            if "auth_id" not in comment or not idPattern.match(comment["auth_id"]):
                return False, "invalid Google UID"
            if "id_token" not in comment:
                return False, "Google ID token missing"
            API.update_google_certs()
            token = API.validate_jwt(comment["id_token"], API.google_certs, self.google_conf.get("client-id"), API.GOOGLE_ISSUERS)
            if not token or "sub" not in token or token["sub"] != comment["auth_id"]:
                return False, "Google ID token validation failed"
        else:
            return False, "unsupported authorization method"

        return True, ""

    def authorize(self, id, data, comment, cookie):

        if comment.get('auth_method') is None:
            # Comment is not authenticated, accept edit if done by
            # same browser session (by inspecting a cookie)
            try:
                rv = self.isso.unsign(cookie)
            except (SignatureExpired, BadSignature):
                raise Forbidden

            if rv[0] != id:
                raise Forbidden

            # verify checksum, mallory might skip cookie deletion when he deletes a comment
            if rv[1] != sha1(comment["text"]):
                raise Forbidden
        else:
            if (data.get('auth_method') != comment['auth_method']
                or data.get('auth_id') != comment.get('auth_id')):
                raise Forbidden

    def parse_users(self, conf):

        self.users = {}
        if conf.has_section("roles"):
            for role in conf.items("roles"):
                role_name, value = role
                role_string, users = value.split(",")
                for user in filter(None, users.split(" ")):
                    self.users[tuple(user.split(":", 1))] = {'role_name': role_name, 'role_string': role_string}

    @xhr
    @requires(str, 'uri')
    def new(self, environ, request, uri):

        data = request.get_json()

        for field in set(data.keys()) - API.ACCEPT:
            data.pop(field)

        for key in ("author", "email", "website", "parent"):
            data.setdefault(key, None)

        valid, reason = self.authenticate(data)
        if not valid:
            return BadRequest(reason)

        valid, reason = self.verify(data)
        if not valid:
            return BadRequest(reason)

        for field in ("author", "email", "website"):
            if data.get(field) is not None:
                data[field] = cgi.escape(data[field])

        if data.get("website"):
            data["website"] = normalize(data["website"])

        data['mode'] = 2 if self.moderated else 1
        data['remote_addr'] = utils.anonymize(str(request.remote_addr))

        with self.isso.lock:
            if uri not in self.threads:
                if 'title' not in data:
                    with http.curl('GET', local("origin") + uri) as resp:
                        if resp and resp.getcode() == 200:
                            uri, title = parse.thread(resp.read(), id=uri)
                        else:
                            return NotFound('URI does not exist %s')
                else:
                    title = data['title']

                thread = self.threads.new(uri, title)
                self.signal("comments.new:new-thread", thread)
            else:
                thread = self.threads[uri]

        # notify extensions that the new comment is about to save
        self.signal("comments.new:before-save", thread, data)

        valid, reason = self.guard.validate(uri, data)
        if not valid:
            self.signal("comments.new:guard", reason)
            raise Forbidden(reason)

        with self.isso.lock:
            rv = self.comments.add(uri, data)

        # notify extension, that the new comment has been successfully saved
        self.signal("comments.new:after-save", thread, rv)

        cookie = functools.partial(dump_cookie,
            value=self.isso.sign([rv["id"], sha1(rv["text"])]),
            max_age=self.conf.getint('max-age'))

        rv["text"] = self.isso.render(rv["text"])
        rv["hash"] = self.hash(rv['email'] or rv['remote_addr'])

        self.cache.set('hash', (rv['email'] or rv['remote_addr']).encode('utf-8'), rv['hash'])

        for key in set(rv.keys()) - API.FIELDS:
            rv.pop(key)

        # success!
        self.signal("comments.new:finish", thread, rv)

        resp = JSON(rv, 202 if rv["mode"] == 2 else 201)
        resp.headers.add("Set-Cookie", cookie(str(rv["id"])))
        resp.headers.add("X-Set-Cookie", cookie("isso-%i" % rv["id"]))
        return resp

    def view(self, environ, request, id):

        rv = self.comments.get(id)
        if rv is None:
            raise NotFound

        for key in set(rv.keys()) - API.FIELDS:
            rv.pop(key)

        if request.args.get('plain', '0') == '0':
            rv['text'] = self.isso.render(rv['text'])

        return JSON(rv, 200)

    @xhr
    def edit(self, environ, request, id):

        data = request.get_json()

        for field in set(data.keys()) - API.ACCEPT:
            data.pop(field)

        valid, reason = self.authenticate(data)
        if not valid:
            return BadRequest(reason)

        valid, reason = self.verify(data)
        if not valid:
            return BadRequest(reason)

        comment = self.comments.get(id)

        if time.time() > comment.get('created') + self.conf.getint('max-age'):
            raise Forbidden

        self.authorize(id, data, comment, request.cookies.get(str(id), ''))

        data['modified'] = time.time()

        for key in set(data.keys()) - API.FIELDS:
            data.pop(key)

        with self.isso.lock:
            rv = self.comments.update(id, data)

        for key in set(rv.keys()) - API.FIELDS:
            rv.pop(key)

        self.signal("comments.edit", rv)

        cookie = functools.partial(dump_cookie,
                value=self.isso.sign([rv["id"], sha1(rv["text"])]),
                max_age=self.conf.getint('max-age'))

        rv["text"] = self.isso.render(rv["text"])

        resp = JSON(rv, 200)
        resp.headers.add("Set-Cookie", cookie(str(rv["id"])))
        resp.headers.add("X-Set-Cookie", cookie("isso-%i" % rv["id"]))
        return resp

    @xhr
    def delete(self, environ, request, id, key=None):

        data = request.get_json()

        for field in set(data.keys()) - API.ACCEPT:
            data.pop(field)

        valid, reason = self.authenticate(data)
        if not valid:
            return BadRequest(reason)

        item = self.comments.get(id)
        if item is None:
            raise NotFound

        self.authorize(id, data, item, request.cookies.get(str(id), ''))

        self.cache.delete('hash', (item['email'] or item['remote_addr']).encode('utf-8'))

        with self.isso.lock:
            rv = self.comments.delete(id)

        if rv:
            for key in set(rv.keys()) - API.FIELDS:
                rv.pop(key)

        self.signal("comments.delete", id)

        resp = JSON(rv, 200)
        cookie = functools.partial(dump_cookie, expires=0, max_age=0)
        resp.headers.add("Set-Cookie", cookie(str(id)))
        resp.headers.add("X-Set-Cookie", cookie("isso-%i" % id))
        return resp

    def moderate(self, environ, request, id, action, key):

        try:
            id = self.isso.unsign(key, max_age=2**32)
        except (BadSignature, SignatureExpired):
            raise Forbidden

        item = self.comments.get(id)

        if item is None:
            raise NotFound

        if request.method == "GET":
            modal = (
                "<!DOCTYPE html>"
                "<html>"
                "<head>"
                "<script>"
                "  if (confirm('%s: Are you sure?')) {"
                "      xhr = new XMLHttpRequest;"
                "      xhr.open('POST', window.location.href);"
                "      xhr.send(null);"
                "  }"
                "</script>" % action.capitalize())

            return Response(modal, 200, content_type="text/html")

        if action == "activate":
            with self.isso.lock:
                self.comments.activate(id)
            self.signal("comments.activate", id)
        else:
            with self.isso.lock:
                self.comments.delete(id)
            self.cache.delete('hash', (item['email'] or item['remote_addr']).encode('utf-8'))
            self.signal("comments.delete", id)

        return Response("Yo", 200)

    @requires(str, 'uri')
    def fetch(self, environ, request, uri):

        args = {
            'uri': uri,
            'after': request.args.get('after', 0)
        }

        if request.args.get('limit') is None:
            args['limit'] = self.max_comments_top
        elif request.args.get('limit')== "inf":
            args['limit'] = None
        else:
            try:
                args['limit'] = int(request.args.get('limit'))
            except ValueError:
                return BadRequest("limit should be integer or 'inf'")

        if request.args.get('parent') is not None:
            try:
                args['parent'] = int(request.args.get('parent'))
                root_id = args['parent']
            except ValueError:
                return BadRequest("parent should be integer")
        else:
            args['parent'] = None
            root_id = None

        plain = request.args.get('plain', '0') == '0'

        reply_counts = self.comments.reply_count(uri, after=args['after'])

        if args['limit'] == 0:
            root_list = []
        else:
            root_list = list(self.comments.fetch(**args))

        if root_id not in reply_counts:
            reply_counts[root_id] = 0

        if request.args.get('nested_limit') is None:
            nested_limit = self.max_comments_nested
        elif request.args.get('nested_limit')== "inf":
            nested_limit = None
        else:
            try:
                nested_limit = int(request.args.get('nested_limit'))
            except ValueError:
                return BadRequest("limit should be integer or 'inf'")

        rv = {
            'id'             : root_id,
            'total_replies'  : reply_counts[root_id],
            'hidden_replies' : reply_counts[root_id] - len(root_list),
            'replies'        : self._process_fetched_list(root_list, plain),
            'config'         : self.public_conf
        }
        # We are only checking for one level deep comments
        if root_id is None:
            for comment in rv['replies']:
                if comment['id'] in reply_counts:
                    comment['total_replies'] = reply_counts[comment['id']]
                    if nested_limit is not None:
                        if nested_limit > 0:
                            args['parent'] = comment['id']
                            args['limit'] = nested_limit
                            replies = list(self.comments.fetch(**args))
                        else:
                            replies = []
                    else:
                        args['parent'] = comment['id']
                        replies = list(self.comments.fetch(**args))
                else:
                    comment['total_replies'] = 0
                    replies = []

                comment['hidden_replies'] = comment['total_replies'] - len(replies)
                comment['replies'] = self._process_fetched_list(replies, plain)

        return JSON(rv, 200)

    def _establish_role(self, item):
        try:
            user = self.users[(item['auth_method'], item['auth_id'])]
        except KeyError:
            item['role_name'] = item['role_string'] = None
            return
        item['role_name'] = user['role_name']
        item['role_string'] = user['role_string']

    def _process_fetched_list(self, fetched_list, plain=False):
        for item in fetched_list:

            key = item['email'] or item['remote_addr']
            val = self.cache.get('hash', key.encode('utf-8'))

            if val is None:
                val = self.hash(key)
                self.cache.set('hash', key.encode('utf-8'), val)

            item['hash'] = val

            self._establish_role(item)

            for key in set(item.keys()) - API.FIELDS:
                item.pop(key)

        if plain:
            for item in fetched_list:
                item['text'] = self.isso.render(item['text'])

        return fetched_list

    @xhr
    def like(self, environ, request, id):

        nv = self.comments.vote(True, id, utils.anonymize(str(request.remote_addr)))
        return JSON(nv, 200)

    @xhr
    def dislike(self, environ, request, id):

        nv = self.comments.vote(False, id, utils.anonymize(str(request.remote_addr)))
        return JSON(nv, 200)

    # TODO: remove someday (replaced by :func:`counts`)
    @requires(str, 'uri')
    def count(self, environ, request, uri):

        rv = self.comments.count(uri)[0]

        if rv == 0:
            raise NotFound

        return JSON(rv, 200)

    def counts(self, environ, request):

        data = request.get_json()

        if not isinstance(data, list) and not all(isinstance(x, str) for x in data):
            raise BadRequest("JSON must be a list of URLs")

        return JSON(self.comments.count(*data), 200)

    def preview(self, environment, request):
        data = request.get_json()

        if "text" not in data or data["text"] is None:
            raise BadRequest("no text given")

        return JSON({'text': self.isso.render(data["text"])}, 200)

    def demo(self, env, req):
        return redirect(get_current_url(env) + '/index.html')
