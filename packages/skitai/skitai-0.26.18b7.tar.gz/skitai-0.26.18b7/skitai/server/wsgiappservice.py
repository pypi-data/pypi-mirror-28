from skitai import __version__, WS_EVT_OPEN, WS_EVT_CLOSE, WS_EVT_INIT
from aquests.lib import pathtool, logger, jwt
from aquests.lib.producers import simple_producer, file_producer
from aquests.lib.athreads import trigger
from aquests.protocols.smtp import composer
from aquests.protocols.http import http_date
from .rpc import cluster_manager, cluster_dist_call
from .dbi import cluster_manager as dcluster_manager, cluster_dist_call as dcluster_dist_call
from skitai import DB_PGSQL, DB_SQLITE3, DB_REDIS, DB_MONGODB
from . import server_info
from . import http_response
import os, sys
import time
import base64
import pickle
from hmac import new as hmac
from hashlib import sha1
from skitai.server.handlers import api_access_handler, vhost_handler
try: 
	from urllib.parse import urljoin
except ImportError:
	from urlparse import urljoin	
import json
from datetime import date
try:
	import xmlrpc.client as xmlrpclib
except ImportError:
	import xmlrpclib	
try: 
	import _thread
except ImportError:
	import thread as _thread	
from skitai import lifetime
from .wastuff.promise import Promise, _Method
from .wastuff.triple_logger import Logger
from .wastuff import django_adaptor
from .wastuff.api import DateEncoder
from multiprocessing import RLock
import random
		
class WAS:
	version = __version__	
	objects = {}	
	_luwatcher = None
	
	lock = RLock ()
	init_time = time.time ()	
	
	#----------------------------------------------------
	# application friendly methods
	#----------------------------------------------------
	
	@classmethod
	def register (cls, name, obj):
		if hasattr (cls, name):
			raise AttributeError ("server object `%s` is already exists" % name)
		cls.objects [name] = obj
		setattr (cls, name, obj)
	
	@classmethod
	def unregister (cls, name):
		del cls.objects [name]
		return delattr (cls, name)
		
	@classmethod
	def add_handler (cls, back, handler, *args, **karg):
		h = handler (cls, *args, **karg)
		if hasattr (cls, "httpserver"):
			cls.httpserver.install_handler (h, back)
		return h
						
	@classmethod
	def add_cluster (cls, clustertype, clustername, clusterlist, ssl = 0, access = []):
		if clustertype and "*" + clustertype in (DB_PGSQL, DB_SQLITE3, DB_REDIS, DB_MONGODB):
			cluster = dcluster_manager.ClusterManager (clustername, clusterlist, "*" + clustertype, access, cls.logger.get ("server"))
			cls.clusters_for_distcall [clustername] = dcluster_dist_call.ClusterDistCallCreator (cluster, cls.logger.get ("server"))
		else:
			cluster = cluster_manager.ClusterManager (clustername, clusterlist, ssl, access, cls.logger.get ("server"))
			cls.clusters_for_distcall [clustername] = cluster_dist_call.ClusterDistCallCreator (cluster, cls.logger.get ("server"), cls.cachefs)
		cls.clusters [clustername] = cluster
	
	def __dir__ (self):
		return self.objects.keys ()
	
	def __str__ (self):
		return "was: Skitai WSGI Appliation Service"
			
	def __detect_cluster (self, clustername):
		try: 
			clustername, uri = clustername.split ("/", 1)
		except ValueError:
			clustername, uri = clustername, ""
		if clustername [0] == "@":
			clustername = clustername [1:]
		return clustername, "/" + uri
	
	def in__dict__ (self, name):
		return name in self.__dict__
	
	def _clone (self, disable_aquests = False):
		new_was = self.__class__ ()
		for k, v in self.__dict__.items ():
			setattr (new_was, k, v)	
		if disable_aquests:
			new_was.VALID_COMMANDS = []
		return new_was
			
	VALID_COMMANDS = [
		"options", "trace", "upload",
		"get", "getjson",
		"delete", "deletejson",
		"post", "postjson",
		"put", "putjson",
		"patch", "patchjson",
		"rpc", "grpc", "ws", "wss", 
		"db", "postgresql", "sqlite3", "redis", "mongodb", "backend",		
	]
	def __getattr__ (self, name):
		# method magic		
		if name in self.VALID_COMMANDS:
			return _Method(self._call, name)
		
		if self.in__dict__ ("app"): # saddle app			
			attr = self.app.create_on_demand (self, name)
			if attr:
				setattr (self, name, attr)
				return attr
		
		try:
			return self.objects [name]
		except KeyError:	
			raise AttributeError ("'was' hasn't attribute '%s'" % name)	
	
	def _call (self, method, args, karg):
		# was.db, 		was.get, 			was.post,			was.put, ...
		# was.db.lb, 	was.get.lb,		was.post.lb,	was.put.lb, ...
		# was.db.map,	was.get.map,	was.post.map,	was.put.map, ...

		uri = None
		if args:		uri = args [0]
		elif karg:	uri = karg.get ("uri", "")
		if not uri:	raise AssertionError ("Missing param uri or cluster name")

		try: 
			command, fn = method.split (".")
		except ValueError: 
			command = method
			if uri [0] == "@": 
				fn = "lb"
			else:
				fn = (command in ("db", "postgresql", "sqlite3", "redis", "mongodb", "backend") and "db" or "rest")

		if fn == "map" and not hasattr (self, "threads"):
			raise AttributeError ("Cannot use Map-Reduce with Single Thread")
		
		if command == "db":
			return getattr (self, "_d" + fn) (*args, **karg)
		elif command in ("postgresql", "sqlite3", "redis", "mongodb", "backend"):
			return getattr (self, "_a" + fn) ("*" + command, *args, **karg)		
		else:	
			return getattr (self, "_" + fn) (command, *args, **karg)
	
	# TXN -----------------------------------------------
	
	def txnid (self):
		return "%s/%s" % (self.request.gtxid, self.request.ltxid)
	
	def rebuild_header (self, header):
		if not header:
			nheader = {}
		elif type (header) is list:
			nheader = {}			
			for k, v in header:
				nheader [k] = v
		else:
			nheader = header
					
		nheader ["X-Gtxn-Id"] = self.request.get_gtxid ()
		nheader ["X-Ltxn-Id"] = self.request.get_ltxid (1)
		return nheader
	
	# Async Requests -----------------------------------------------
		
	def _rest (self, method, uri, data = None, auth = None, headers = None, meta = None, use_cache = True, filter = None, callback = None, timeout = 10):
		return self.clusters_for_distcall ["__socketpool__"].Server (uri, data, method, self.rebuild_header (headers), auth, meta, use_cache, False, filter, callback, timeout)
	
	def _crest (self, mapreduce = False, method = None, uri = None, data = None, auth = None, headers = None, meta = None, use_cache = True, filter = None, callback = None, timeout = 10):
		clustername, uri = self.__detect_cluster (uri)
		return self.clusters_for_distcall [clustername].Server (uri, data, method, self.rebuild_header (headers), auth, meta, use_cache, mapreduce, filter, callback, timeout)
				
	def _lb (self, *args, **karg):
		return self._crest (False, *args, **karg)
		
	def _map (self, *args, **karg):
		return self._crest (True, *args, **karg)
		
	def _ddb (self, server, dbname = "", auth = None, dbtype = DB_PGSQL, meta = None, use_cache = True, filter = None, callback = None, timeout = 10):		
		return self.clusters_for_distcall ["__dbpool__"].Server (server, dbname, auth, dbtype, meta, use_cache, False, filter, callback, timeout)
	
	def _cddb (self, mapreduce = False, clustername = None, meta = None, use_cache = True, filter = None, callback = None, timeout = 10):
		if mapreduce and callback: raise RuntimeError ("Cannot use callback with Map-Reduce")
		clustername = self.__detect_cluster (clustername) [0]
		return self.clusters_for_distcall [clustername].Server (None, None, None, None, meta, use_cache, mapreduce, filter, callback, timeout)	
	
	def _dlb (self, *args, **karg):
		return self._cddb (False, *args, **karg)
	
	def _dmap (self, *args, **karg):
		return self._cddb (True, *args, **karg)
	
	def _adb (self, dbtype, server, dbname = "", auth = None, meta = None, use_cache = True, filter = None, callback = None, timeout = 10):
		return self._ddb (server, dbname, auth, dbtype, meta, use_cache, filter, callback, timeout)
	
	def _alb (self, dbtype, *args, **karg):
		return self._cddb (False, *args, **karg)
	
	def _amap (self, dbtype, *args, **karg):
		return self._cddb (True, *args, **karg)
	
	# Response Helpers --------------------------------------------
		
	def render (self, template_file, _do_not_use_this_variable_name_ = {}, **karg):
		return self.app.render (self, template_file, _do_not_use_this_variable_name_, **karg)
	
	def ab (self, thing, *args, **karg):
		if thing.startswith ("/") or thing.find (".") == -1:
			return self.app.build_url (thing, *args, **karg)
		return self.apps.build_url (thing, *args, **karg)
	
	REDIRECT_TEMPLATE =  (
		"<head><title>%s</title></head>"
		"<body><h1>%s</h1>"
		"This document may be found " 
		'<a HREF="%s">here</a></body>'
	)		
	def redirect (self, url, status = "302 Object Moved", body = None, headers = None):
		redirect_headers = [
			("Location", url), 
			("Cache-Control", "max-age=0"), 
			("Expires", http_date.build_http_date (time.time ()))
		]
		if type (headers) is list:
			redirect_headers += headers
		if not body:
			body = self.REDIRECT_TEMPLATE % (status, status, url)			
		return self.response (status, body, redirect_headers)
	
	def promise (self, handler, **karg):
		self.response.set_streaming ()
		return Promise (self, handler, **karg)
	
	def email (self, subject, snd, rcpt):
		if composer.Composer.SAVE_PATH is None:
			composer.Composer.SAVE_PATH = os.path.join ("/tmp/skitai/smtpda", "mail", "spool")
			pathtool.mkdir (composer.Composer.SAVE_PATH)			
		return composer.Composer (subject, snd, rcpt)
	
	# Event -------------------------------------------------
	
	def broadcast (self, event, *args, **kargs):
		return self.apps.bus.emit (event, self, *args, **kargs)
	
	def setlu (self, name, *args, **karg):
		self._luwatcher.set (name, time.time (), karg.get ("x_ignore", False))
		self.broadcast ("model-changed", *args, **karg)
		self.broadcast ("model-changed:%s" % name, *args, **karg)			
		
	def getlu (self, *names):
		mtimes = []
		for name in names:
			mtime = self._luwatcher.get (name, self.init_time)
			mtimes.append (mtime)
		return max (mtimes)
		
	# Websocket -----------------------------------------------
	
	def wsconfig (self, spec, timeout = 60, encoding = "text"):
		self.env ["websocket.config"] = (spec, timeout, encoding)
		return ""
		
	def wsinit (self):
		return self.env.get ('websocket.event') == WS_EVT_INIT
	
	def wsopened (self):
		return self.env.get ('websocket.event') == WS_EVT_OPEN
	
	def wsclosed (self):
		return self.env.get ('websocket.event') == WS_EVT_CLOSE
	
	def wshasevent (self):
		return self.env.get ('websocket.event')
	
	def wsclient (self):
		return self.env.get ('websocket.client')	
	
	# Systen Functions -------------------------------------
	
	def log (self, msg, category = "info", at = "app"):
		self.logger (at, msg, "%s:%s" % (category, self.txnid ()))
		
	def traceback (self, id = "", at = "app"):
		if not id:
			id = self.txnid ()
		self.logger.trace (at, id)
	
	def status (self, flt = None, fancy = True):
		return server_info.make (self, flt, fancy)
	
	def restart (self, timeout = 0):
		lifetime.shutdown (3, timeout)
	
	def shutdown (self, timeout = 0):
		lifetime.shutdown (0, timeout)
	
	# Tokens  -----------------------------------------------
	
	def tokenize (self, obj):
		b = base64.b64encode (pickle.dumps (obj, 1)).rstrip (b'=')
		mac = hmac (self.app.securekey.encode ("utf8"), None, sha1)
		mac.update (b)
		return (base64.b64encode(mac.digest()).strip() + b"?" + b).rstrip (b'=').decode ("utf8")
	
	def untokenize (self, string):
		def adjust_padding (s):
			paddings = 4 - (len (s) % 4)
			if paddings != 4:
				s += b"=" * paddings
			return s
		
		string = string.encode ("utf8")
		base64_hash, data = string.split(b'?', 1)
		client_hash = base64.b64decode(adjust_padding (base64_hash))
		mac = hmac(self.app.securekey.encode ("utf8"), None, sha1)		
		mac.update(data)
		if client_hash != mac.digest():
			return
		return pickle.loads (base64.b64decode (adjust_padding (data)))
		
	@property
	def csrf_token (self):
		if "_csrf_token" not in self.session:
			self.session ["_csrf_token"] = hex (random.getrandbits (64))
		return self.session ["_csrf_token"]

	@property
	def csrf_token_input (self):
		return '<input type="hidden" name="_csrf_token" value="{}">'.format (self.csrf_token)
	
	def csrf_verify (self):
		if not self.request.args.get ("_csrf_token"):
			return False
		token = self.request.args ["_csrf_token"]
		if self.csrf_token == token:
			del self.session ["_csrf_token"]
			return True
		return False
	
	# Proxy & Adaptor  -----------------------------------------------
	
	@property
	def sqlmap (self):
		return self.app.sqlmap
	
	@property
	def django (self):
		if hasattr (self.request, "django"):
			return self.request.django
		self.request.django = django_adaptor.request (self)
		return self.request.django
			
	# Will Be Deprecated --------------------------------------------------	
	
	def render_ei (self, exc_info, format = 0):
		return http_response.catch (format, exc_info)
	
	def togrpc (self, obj):
		return obj.SerializeToString ()
	
	def fromgrpc (self, message, obj):
		return message.ParseFromString (obj)
		
	def tojson (self, obj):
		return json.dumps (obj, cls = DateEncoder)
		
	def toxml (self, obj):
		return xmlrpclib.dumps (obj, methodresponse = False, allow_none = True, encoding = "utf8")	
	
	def fromjson (self, obj):
		if type (obj) is bytes:
			obj = obj.decode ('utf8')
		return json.loads (obj)
	
	def fromxml (self, obj, use_datetime = 0):
		return xmlrpclib.loads (obj)
	
	def fstream (self, path, mimetype = 'application/octet-stream'):	
		self.response.set_header ('Content-Type',  mimetype)
		self.response.set_header ('Content-Length', str (os.path.getsize (path)))	
		return file_producer (open (path, "rb"))
			
	def jstream (self, obj, key = None):
		self.response.set_header ("Content-Type", "application/json")
		if key:
			# for single skeleton data is not dict
			return self.tojson ({key: obj})
		else:
			return self.tojson (obj)		
	
	def xstream (self, obj, use_datetime = 0):			
		self.response.set_header ("Content-Type", "text/xml")
		return self.toxml (obj, use_datetime)
	
	def gstream (self, obj):
		self.response.set_header ("Content-Type", "application/grpc")
		return self.togrpc (obj)
		