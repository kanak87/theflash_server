from base_request import RequestBase

class RequestUpdateUserPosition(RequestBase):
	def processData(self, data):
		result = { }
		conn = None
		cursor = None

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
				result['result'] = 0
			else:
				raise Exception("db replace error")

		except Exception as e:
			result['result'] = -1
			result['error_msg'] = str(e)

		finally:
			if not cursor is None:
				cursor.close()
			if not conn is None:
				conn.close()

		return result