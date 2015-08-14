from flask import json
from flask.ext.mysql import MySQL
from redis import Redis
import tornado.web
import os

class RequestBase(tornado.web.RequestHandler):
	def initialize(self, mysql, redis):
		self.mysql = mysql
		self.redis = redis

	def getRequestJsonData(self):
		data = None
		result = { }

		try:
			data = json.loads(self.get_argument('data'))

		except Exception as e:
			print e

			result['result'] = -1
			result['error_msg'] = str(e)

			self.write(json.dumps(result))

		return data

	def processData(self, jsonData):
		return

	def get(self):
		return self.post()

	def post(self):
		jsonData = self.getRequestJsonData()
		if jsonData == None:
			return

		result = self.processData(jsonData)
		self.write(json.dumps(result))

