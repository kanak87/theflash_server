from base_request import RequestBase
from database.db_functions import get_user_id
from database.db_functions import add_new_user
from database.redis_functions import set_user_name


class RequestAuth(RequestBase):
    def process_data(self, data):
        result = {}
        conn = None
        cursor = None

        try:
            user_name = data['user_name']
            social_id = data['social_id']

            if user_name == "":
                raise Exception("empty user_name")
            if social_id == "":
                raise Exception("empty social_id")

            conn = self.mysql.connect()
            cursor = conn.cursor()

            user_id = get_user_id(user_name, social_id, conn, cursor, False)

            if user_id is None:
                add_new_user(user_name, social_id, conn, cursor)
                user_id = get_user_id(user_name, social_id, conn, cursor)

            r = self.get_redis_connection()
            set_user_name(r, user_id, user_name)

            result['result'] = 0
            result['user_id'] = user_id

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
