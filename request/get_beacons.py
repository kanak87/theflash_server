from flask import json
from flask.ext.mysql import MySQL
from redis import Redis
from datetime import timedelta, datetime
import tornado.web
import os

class RequestGetBeacons(tornado.web.RequestHandler):
	def initialize(self, mysql, redis):
		self.mysql = mysql
		self.redis = redis

	def get(self):
		return self.post()

	def post(self):
		result = []
		conn = None
		cursor = None

		try:
			data = json.loads(self.get_argument('data'))

		except Exception as e:
			print e

			result.append({'result' : -1})
			result.append({'error_msg' : str(e)})

			self.write(json.dumps(result))
			pass

		try:
			conn = self.mysql.connect()
			cursor = conn.cursor()

			cursor.execute('select * from beacon')

			beacons = []

			columns = tuple([d[0] for d in cursor.description])

			for row in cursor:
				beacons.append(dict(zip(columns, row)))

			result.append({'result' : 0})
			result.append({'beacons' : beacons})

		except Exception as e:
			print e
			result.append({'result' : -1})
			result.append({'error_msg' : str(e)})
		finally:
			if cursor is not None:
				cursor.close()
			if conn is not None:
				conn.close()

		self.write(json.dumps(result))
