from base_request import RequestBase
from request.db_function import get_user_id
from request.db_function import add_new_user


class RequestAuth(RequestBase):
    def process_data(self, data):
        result = {}

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

            result['result'] = 0
            result['user_id'] = user_id

        except Exception as e:
            print e

            result['result'] = -1
            result['error_msg'] = str(e)

        return result
