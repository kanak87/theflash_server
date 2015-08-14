from base_request import RequestBase
import os

def generateUserToken():
	return os.urandom(20).encode('hex')

class RequestAuth(RequestBase):
	def processData(self, data):
		result = { }
		user_name = ""
		isRegister = False
		hasError = False

		try:
			user_name = data['user_name']

		except Exception as e:
			result['result'] = -1
			result['error_msg'] = str(e)
			hasError = True

		if hasError == True:
			return result

		# Check registration
		try:
			user_id = data['user_id']
			user_token = data['user_token']

		except Exception as e:
			isRegister = True

		if isRegister == True:
			result = self.processRegistration(user_name)
		else:
			result = self.processLogin(user_id, user_name, user_token)

		return result

	def processRegistration(self, user_name):
		result = { }
		conn = None
		cursor = None

		try:
			if user_name == "":
				raise Exception("empty user_name")

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

			result['result'] = 0
			result['user_id'] = user_id
			result['user_name'] = user_name
			result['user_token'] = user_token

		except Exception as e:
			result['result'] = -1
			result['error_msg'] = str(e)

		finally:
			if cursor is not None:
				cursor.close()
			if conn is not None:
				conn.close()

		return result

	def processLogin(self, user_id, user_name, user_token):
		result = { }
		conn = None
		cursor = None

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

			result['result'] = 0
			result['user_id'] = user_id
			result['user_name'] = user_name
			result['user_token'] = user_token

		except Exception as e:
			result['result'] = -1
			result['error_msg'] = str(e)

		finally:
			if cursor is not None:
				cursor.close()
			if conn is not None:
				conn.close()

		return result