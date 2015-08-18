from base_request import RequestBase
from datetime import timedelta, datetime
from database.redis_functions import get_users, remove_users

user_columns = ['user_id', 'beacon_id', 'distance']
expired_second = 60


class RequestGetUsers(RequestBase):
    def process_data(self, data):
        result = {}
        try:
            r = self.get_redis_connection();

            users = get_users(r)
            alive_users = []
            expired_users = []

            now_time = datetime.today()
            expire_time_delta = timedelta(seconds=expired_second)

            for user in users:
                if now_time > user[3] + expire_time_delta:
                    expired_users.append(user[0])
                else:
                    alive_users.append(dict(zip(user_columns, user[:3])))

            if len(expired_users) > 0:
                remove_users(r, expired_users)

            result['result'] = 0
            result['users'] = alive_users

        except Exception as e:
            print e
            result['result'] = -1
            result['error_msg'] = str(e)

        return result
