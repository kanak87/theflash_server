import logging
from flask import Flask
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import tornado.web
import redis
from mysql.connector.pooling import MySQLConnectionPool

from database.cache_functions import beacon_cache, user_cache
from request.auth import RequestAuth
from request.base_request import RequestPage
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

        dbconfig = { "user" : settings.db_user_name,
                     "password" : settings.db_password,
                     "database" : settings.db_name,
                     "host" : settings.db_host
                     }
        self.mysql_pool = MySQLConnectionPool(pool_name=None, pool_size=4, pool_reset_session=True, **dbconfig)
        logging.info('Database Initialized')

        self.redis_pool = redis.ConnectionPool(host=settings.redis_host, port=settings.redis_port, db=0)
        logging.info('Redis Initialized')

        self.application = tornado.web.Application([
            (r"/auth", RequestAuth, dict(mysql_pool=self.mysql_pool, redis_pool=self.redis_pool)),
            (r"/get_users", RequestGetUsers, dict(mysql_pool=self.mysql_pool, redis_pool=self.redis_pool)),
            (r"/get_beacons", RequestGetBeacons, dict(mysql_pool=self.mysql_pool, redis_pool=self.redis_pool)),
            (r"/update_user_pos", RequestUpdateUserPosition, dict(mysql_pool=self.mysql_pool, redis_pool=self.redis_pool)),
            (r"/register_beacon", RequestRegisterBeacon, dict(mysql_pool=self.mysql_pool, redis_pool=self.redis_pool)),
            (r"/unregister_beacon", RequestUnregisterBeacon, dict(mysql_pool=self.mysql_pool, redis_pool=self.redis_pool)),
            (r"/", RequestPage, dict(mysql_pool=self.mysql_pool, redis_pool=self.redis_pool, page_name="index.html")),
            (r"/manage", RequestPage, dict(mysql_pool=self.mysql_pool, redis_pool=self.redis_pool, page_name="manage.html")),
            (r"/about", RequestPage, dict(mysql_pool=self.mysql_pool, redis_pool=self.redis_pool, page_name="about.html")),
        ],
            debug=debug,
            autoreload=debug,
            static_path=settings.static_path
        )
        logging.info('Application Initialized')

        self.init_cache()

    def init_cache(self):
        conn = None
        cursor = None

        try:
            conn = self.mysql_pool.get_connection()
            cursor = conn.cursor()

            beacon_cache(conn, cursor, self.redis_pool)
            user_cache(conn, cursor, self.redis_pool)

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