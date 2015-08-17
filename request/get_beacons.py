from base_request import RequestBase


class RequestGetBeacons(RequestBase):
    def process_data(self, data):
        result = {}
        conn = None
        cursor = None

        try:
            conn = self.mysql.connect()
            cursor = conn.cursor()

            cursor.execute('select * from beacon')

            beacons = []

            columns = tuple([d[0] for d in cursor.description])

            for row in cursor:
                beacons.append(dict(zip(columns, row)))

            result['result'] = 0
            result['beacons'] = beacons

        except Exception as e:
            result['result'] = -1
            result['error_msg'] = str(e)

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

        return result
