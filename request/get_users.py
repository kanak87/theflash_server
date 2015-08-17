from base_request import RequestBase
from datetime import timedelta, datetime


class RequestGetUsers(RequestBase):
    def process_data(self, data):
        result = {}
        try:
            conn = self.mysql.connect()
            cursor = conn.cursor()
            cursor.execute('select * from position')

            users = []
            expired_users = []

            columns = list([d[0] for d in cursor.description])
            columns.pop()

            now_time = datetime.today()
            expire_time_delta = timedelta(seconds=60)

            for row in cursor:
                if now_time > row[3] + expire_time_delta:
                    expired_users.append(row[0])
                else:
                    users.append(dict(zip(columns, row)))

            if len(expired_users) > 0:
                delete_users_query = "delete from position where user_id in ("
                delete_users_query += "'" + str(expired_users[0]) + "'"

                for expired_user_id in expired_users[1:]:
                    delete_users_query += ",'" + expired_user_id + "'"

                delete_users_query += ")"

                queryResult = cursor.execute(delete_users_query)
                conn.commit()

                result_data = cursor.fetchone()

                if result_data is not None or cursor.rowcount < 1:
                    raise Exception('delete queury error')

            result['result'] = 0
            result['users'] = users

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
