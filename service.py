import logging

from flask import Flask
from flask.ext.mysql import MySQL
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import tornado.web
import redis

from database.cache_functions import beacon_cache
from request.auth import RequestAuth
from request.get_users import RequestGetUsers
from request.get_beacons import RequestGetBeacons
from request.update_user_position import RequestUpdateUserPosition
from request.register_beacon import RequestRegisterBeacon
from request.unregister_beacon import RequestUnregisterBeacon
import settings


class TheFlashServer:
    def __init__(self, debug=False):
        if debug:
            logging.info('Initializing The Flash Server as debug mode')
        else:
            logging.info('Initializing The Flash Server as production mode')

        self.debug = debug

        self.app = Flask(__name__)
        logging.info('Flask Initialized')

        self.mysql = MySQL()

        self.app.config['MYSQL_DATABASE_USER'] = settings.db_user_name
        self.app.config['MYSQL_DATABASE_PASSWORD'] = settings.db_password
        self.app.config['MYSQL_DATABASE_DB'] = settings.db_name
        self.app.config['MYSQL_DATABASE_HOST'] = settings.db_host
        self.mysql.init_app(self.app)
        logging.info('Database Initialized')

        self.redis_pool = redis.ConnectionPool(host=settings.redis_host, port=settings.redis_port, db=0)
        logging.info('Redis Initialized')

        self.application = tornado.web.Application([
            (r"/auth", RequestAuth, dict(mysql=self.mysql, redis_pool=self.redis_pool)),
            (r"/get_users", RequestGetUsers, dict(mysql=self.mysql, redis_pool=self.redis_pool)),
            (r"/get_beacons", RequestGetBeacons, dict(mysql=self.mysql, redis_pool=self.redis_pool)),
            (r"/update_user_pos", RequestUpdateUserPosition, dict(mysql=self.mysql, redis_pool=self.redis_pool)),
            (r"/register_beacon", RequestRegisterBeacon, dict(mysql=self.mysql, redis_pool=self.redis_pool)),
            (r"/unregister_beacon", RequestUnregisterBeacon, dict(mysql=self.mysql, redis_pool=self.redis_pool)),
        ],
            debug=debug,
            autoreload=debug,
        )
        logging.info('Application Initialized')

        self.init_cache()

    def init_cache(self):
        conn = None
        cursor = None

        try:
            conn = self.mysql.connect()
            cursor = conn.cursor()

            beacon_cache(conn, cursor, self.redis_pool)

        except Exception as e:
            logging.error(str(e))
            raise

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    def start(self):
        logging.info('The Flash Server Start')

        server = tornado.httpserver.HTTPServer(self.application)
        if self.debug:
            print '- Start as debug mode'
            server.listen(settings.service_port)
        else:
            server.bind(settings.service_port)
            server.start(0)

        IOLoop.current().start()
