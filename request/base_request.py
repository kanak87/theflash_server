import os

from flask import json
import redis
import tornado.web

from settings import template_path


class RequestBase(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def initialize(self, mysql_pool, redis_pool):
        self.redis_pool = redis_pool
        self.mysql_pool = mysql_pool

    def get_mysql_connection(self):
        return self.mysql_pool.get_connection()

    def get_redis_connection(self):
        return redis.Redis(connection_pool=self.redis_pool)

    def get_request_json_data(self):
        data = None
        result = {}

        try:
            data = json.loads(self.get_argument('data'))

        except Exception as e:
            print e

            result['result'] = -1
            result['error_msg'] = str(e)

            self.write(json.dumps(result))

        return data

    def process_data(self, jsonData):
        return

    def get(self):
        return self.post()

    def post(self):
        json_data = self.get_request_json_data()
        if json_data is None:
            return

        result = self.process_data(json_data)
        self.write(json.dumps(result))


class RequestPage(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def initialize(self, mysql_pool, redis_pool, page_name):
        self.redis_pool = redis_pool
        self.mysql_pool = mysql_pool
        self.page_path = os.path.join(template_path, page_name)

    def get_mysql_connection(self):
        return self.mysql_pool.get_connection()

    def get_redis_connection(self):
        return redis.Redis(connection_pool=self.redis_pool)

    def get(self):
        return self.post()

    def post(self):
        self.render(self.page_path)
