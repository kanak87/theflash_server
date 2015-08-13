from flask import json
from flask.ext.mysql import MySQL
from redis import Redis
import tornado.web
import os

def generateUserToken():
	return os.urandom(20).encode('hex')

class RequestAuth(tornado.web.RequestHandler):
	def initialize(self, mysql, redis):
		self.mysql = mysql
		self.redis = redis

	def get(self):
		return self.post()

	def post(self):
		result = []
		conn = None
		cursor = None
		isRegister = False

		try:
			data = json.loads(self.get_argument('data'))
			user_name = data['user_name']

		except Exception as e:
			print e

			result.append({'result' : -1})
			result.append({'error_msg' : str(e)})

			self.write(json.dumps(result))
			pass

		# Check registration
		try:
			user_id = data['user_id']
			user_token = data['user_token']

		except Exception as e:
			isRegister = True

		# Registration
		if isRegister == True:
			try:
				user_token = generateUserToken()

				conn = self.mysql.connect()
				cursor = conn.cursor()

				queryResult = cursor.execute("insert into user (user_name, user_token, registration_time) values('%s', '%s', now())" % (user_name, user_token))
				conn.commit()
				resultData = cursor.fetchone()

				if not (resultData == None and cursor.rowcount >= 1):
					raise Exception("db error, insert new user")

				queryResult = cursor.execute("select user_id from user where user_name='%s' and user_token='%s'" % (user_name, user_token))
				resultData = cursor.fetchone()

				if resultData == None or cursor.rowcount == 0:
					raise Exception("db error, select new user")
				else:
					user_id = int(resultData[0])

				result.append({'result' : 0})
				result.append({'user_id' : user_id})
				result.append({'user_name' : user_name})
				result.append({'user_token' : user_token})

			except Exception as e:
				print e

				result.append({'result' : -1})
				result.append({'error_msg' : str(e)})

			finally:
				if cursor is not None:
					cursor.close()
				if conn is not None:
					conn.close()

		# Login Process
		else:
			try:
				conn = self.mysql.connect()
				cursor = conn.cursor()

				queryResult = cursor.execute("select user_id from user where user_name='%s' and user_token='%s'" % (user_name, user_token))

				resultData = cursor.fetchone()
				if resultData == None or cursor.rowcount != 1:
					raise Exception('db error, select new user')
				else:
					result_user_id = int(resultData[0])

				if user_id != result_user_id:
					raise Exception('invalid user')

				result.append({'result' : 0})
				result.append({'user_id' : user_id})
				result.append({'user_name' : user_name})
				result.append({'user_token' : user_token})

			except Exception as e:
				result.append({'result' : -1})
				result.append({'error_msg' : str(e)})

				self.write(json.dumps(result))
			finally:
				if cursor is not None:
					cursor.close()
				if conn is not None:
					conn.close()

		self.write(json.dumps(result))