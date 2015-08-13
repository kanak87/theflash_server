from flask import json
from flask.ext.mysql import MySQL
from redis import Redis
from datetime import timedelta, datetime
import tornado.web
import os

class RequestGetUsers(tornado.web.RequestHandler):
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
			cursor.execute('select * from position')

			users = []
			expired_users = []

			columns = list([d[0] for d in cursor.description])
			columns.pop()

			nowTime = datetime.today()
			expireTimeDelta = timedelta(seconds=60)

			for row in cursor:
				if nowTime > row[3] + expireTimeDelta:
					expired_users.append(row[0])
				else:
					users.append(dict(zip(columns, row)))

			delete_users_query = ""

			if len(expired_users) > 0:
				delete_users_query = "delete from position where user_id in ("
				delete_users_query += "'" + str(expired_users[0]) + "'"

				for expired_user_id in expired_users[1:]:
					delete_users_query += ",'" + expired_user_id + "'"

				delete_users_query += ")"

				queryResult = cursor.execute(delete_users_query)
				conn.commit()

				resultData = cursor.fetchone()
				
				if resultData != None or cursor.rowcount < 1:
					raise Exception('delete queury error')

			result.append({'result' : 0})
			result.append({'users' : users})

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
