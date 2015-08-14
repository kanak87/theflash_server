from base_request import RequestBase

class RequestUnregisterBeacon(RequestBase):
	def processData(self, data):
		result = { }
		conn = None
		cursor = None

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
				result['result'] = 0
			else:
				raise Exception("already deleted beacon")

		except Exception as e:
			result['result'] = -1
			result['error_msg'] = str(e)

		finally:
			if not cursor is None:
				cursor.close()
			if not conn is None:
				conn.close()

		return result