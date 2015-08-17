from base_request import RequestBase


class RequestUpdateUserPosition(RequestBase):
    def process_data(self, data):
        result = {}
        conn = None
        cursor = None

        try:
            user_id = data['user_id']
            beacon_id = data['beacon_id']
            distance = data['distance']

            conn = self.mysql.connect()
            cursor = conn.cursor()

            queryResult = cursor.execute(
                "replace into position (user_id, beacon_id, distance, update_timestamp) values('%s', %d, %d, now())" % (user_id, beacon_id, distance))
            conn.commit()

            result_data = cursor.fetchone()

            if result_data is None and cursor.rowcount >= 1:
                result['result'] = 0
            else:
                raise Exception("db replace error")

        except Exception as e:
            result['result'] = -1
            result['error_msg'] = str(e)

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

        return result
