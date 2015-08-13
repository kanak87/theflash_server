from flask import json
from flask.ext.mysql import MySQL
from redis import Redis
from datetime import timedelta, datetime
import tornado.web

class RequestUnregisterBeacon(tornado.web.RequestHandler):
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
			mac_addr = data['mac_addr']
			advertising_data = data['ad_data']

			conn = self.mysql.connect()
			cursor = conn.cursor()
			
			queryResult = cursor.execute("delete from theflash.beacon where mac_addr='%s' and advertising_data='%s'" %
			 (mac_addr, advertising_data))
			conn.commit()

			resultData = cursor.fetchone()
			
			if resultData == None and cursor.rowcount == 1:
				result.append({'result' : 0})
			else:
				raise Exception("already deleted beacon")

		except Exception as e:
			result.append({'result' : -1})
			result.append({'error_msg' : str(e)})

		finally:
			if not cursor is None:
				cursor.close()
			if not conn is None:
				conn.close()

		self.write(json.dumps(result))