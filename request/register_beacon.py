from base_request import RequestBase

class RequestRegisterBeacon(RequestBase):
	def processData(self, data):
		result = { }
		conn = None
		cursor = None

		try:
			mac_addr = data['mac_addr']
			advertising_data = data['ad_data']
			x = data['x']
			y = data['y']

			conn = self.mysql.connect()
			cursor = conn.cursor()

			queryResult = cursor.execute("insert into theflash.beacon (mac_addr, advertising_data, x, y) values('%s', '%s', %s, %s)" %
			 (mac_addr, advertising_data, x, y))
			conn.commit()

			resultData = cursor.fetchone()
			
			if resultData == None and cursor.rowcount == 1:
				result['result'] = 0
			else:
				raise Exception("beacon insert error")

		except Exception as e:
			result['result'] = -1
			result['error_msg'] = str(e)

		finally:
			if not cursor is None:
				cursor.close()
			if not conn is None:
				conn.close()

		return result