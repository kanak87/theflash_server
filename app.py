from flask import Flask, json
from flask.ext.mysql import MySQL
from redis import Redis
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import tornado.web
import settings
from request.auth import RequestAuth
from request.get_users import RequestGetUsers
from request.get_beacons import RequestGetBeacons
from request.update_user_position import RequestUpdateUserPosition
from request.register_beacon import RequestRegisterBeacon
from request.unregister_beacon import RequestUnregisterBeacon 

app = Flask(__name__)
redis = Redis()
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = settings.db_user_name
app.config['MYSQL_DATABASE_PASSWORD'] = settings.db_password
app.config['MYSQL_DATABASE_DB'] = settings.db_name
app.config['MYSQL_DATABASE_HOST'] = settings.db_host

mysql.init_app(app)

if __name__ == "__main__":
	application = tornado.web.Application([
		(r"/auth", RequestAuth, dict(mysql = mysql, redis = redis)),
		(r"/get_users", RequestGetUsers, dict(mysql = mysql, redis = redis)),
		(r"/get_beacons", RequestGetBeacons, dict(mysql = mysql, redis = redis)),
		(r"/update_user_pos", RequestUpdateUserPosition, dict(mysql = mysql, redis = redis)),
		(r"/register_beacon", RequestRegisterBeacon, dict(mysql = mysql, redis = redis)),
		(r"/unregister_beacon", RequestUnregisterBeacon, dict(mysql = mysql, redis = redis)),
		])

	server = tornado.httpserver.HTTPServer(application)
	server.bind(14000)
	server.start(1)
	IOLoop.current().start()
