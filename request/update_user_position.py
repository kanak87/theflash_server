from flask import json
from flask.ext.mysql import MySQL
from redis import Redis
from datetime import timedelta, datetime
import tornado.web

class RequestUpdateUserPosition(tornado.web.RequestHandler):
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
			user_id = data['user_id']
			x = data['x']
			y = data['y']

			conn = self.mysql.connect()
			cursor = conn.cursor()

			queryResult = cursor.execute("replace into position (user_id, x, y, update_timestamp) values('%s', %d, %d, now())" % (user_id, x, y))
			conn.commit()

			resultData = cursor.fetchone()

			if resultData == None and cursor.rowcount >= 1:
				result.append({'result' : 0})
			else:
				raise Exception("db replace error")

		except Exception as e:
			result.append({'result' : -1})
			result.append({'error_msg' : str(e)})

		finally:
			if not cursor is None:
				cursor.close()
			if not conn is None:
				conn.close()

		self.write(json.dumps(result))