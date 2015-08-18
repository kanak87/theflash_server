from base_request import RequestBase
from database.redis_functions import insert_user


class RequestUpdateUserPosition(RequestBase):
    def process_data(self, data):
        result = {}
        conn = None
        cursor = None

        try:
            user_id = data['user_id']
            beacon_id = data['beacon_id']
            distance = data['distance']

            r = self.get_redis_connection()

            if not insert_user(r, user_id, beacon_id, distance):
                raise Exception("Redis insert_user Error")

            result['result'] = 0

        except Exception as e:
            print e
            result['result'] = -1
            result['error_msg'] = str(e)

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

        return result
