'''
from base_request import RequestBase
from database.db_functions import get_beacon_id
from database.redis_functions import remove_beacon


class RequestUnregisterBeacon(RequestBase):
    def process_data(self, data):
        result = {}
        conn = None
        cursor = None

        try:
            mac_addr = data['mac_addr']
            advertising_data = data['ad_data']

            conn = self.mysql.connect()
            cursor = conn.cursor()

            beacon_id = get_beacon_id(mac_addr, advertising_data, conn, cursor)

            queryResult = cursor.execute("delete from theflash.beacon where mac_addr='%s' and advertising_data='%s'" % (mac_addr, advertising_data))
            conn.commit()

            result_data = cursor.fetchone()

            if result_data is None and cursor.rowcount == 1:
                result['result'] = 0
            else:
                raise Exception("Not exist beacon")

            r = self.get_redis_connection()
            remove_beacon(r, beacon_id)

        except Exception as e:
            result['result'] = -1
            result['error_msg'] = str(e)

        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

        return result
'''

from base_request import RequestBase
from database.db_functions import get_beacon_id
from database.redis_functions import remove_beacon


class RequestUnregisterBeacon(RequestBase):
    def process_data(self, data):
        result = {}
        conn = None
        cursor = None

        try:
            mac_addr = data['mac_addr']
            advertising_data = data['ad_data']

            conn = self.get_mysql_connection()
            cursor = conn.cursor()

            beacon_id = get_beacon_id(mac_addr, advertising_data, conn, cursor, False)
            if beacon_id is None:
                raise Exception("Not exist beacon")

            queryResult = cursor.execute("delete from theflash.beacon where mac_addr='%s' and advertising_data='%s'" % (mac_addr, advertising_data))
            conn.commit()

            result_data = cursor.fetchone()

            if result_data is None and cursor.rowcount == 1:
                result['result'] = 0
            else:
                raise Exception("Not exist beacon")

            r = self.get_redis_connection()
            remove_beacon(r, beacon_id)

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