from flask import json
import tornado.web


class RequestBase(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def initialize(self, mysql, redis):
        self.redis = redis
        self.mysql = mysql

    def get_request_json_data(self):
        data = None
        result = {}

        try:
            data = json.loads(self.get_argument('data'))

        except Exception as e:
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
