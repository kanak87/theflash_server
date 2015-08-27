from base_request import RequestBase
from database.cache_functions import beacon_cache
from database.db_functions import get_beacon_id
from database.redis_functions import insert_beacon


class RequestRegisterBeacon(RequestBase):
    def process_data(self, data):
        result = {}
        conn = None
        cursor = None

        try:
            mac_addr = data['mac_addr']
            advertising_data = data['ad_data']
            x = data['x']
            y = data['y']

            conn = self.get_mysql_connection()
            cursor = conn.cursor()

            queryResult = cursor.execute("insert into theflash.beacon (mac_addr, advertising_data, x, y) values('%s', '%s', %s, %s)" % (mac_addr, advertising_data, x, y))
            conn.commit()

            result_data = cursor.fetchone()

            if result_data is None and cursor.rowcount == 1:
                result['result'] = 0
            else:
                raise Exception("beacon insert error")

            beacon_id = get_beacon_id(mac_addr, advertising_data, cursor, cursor)

            r = self.get_redis_connection()
            insert_beacon(r, beacon_id, mac_addr, advertising_data, x, y)

        except Exception as e:
            print e
            result['result'] = -1
            result['error_msg'] = str(e)

        finally:
            if not cursor is None:
                cursor.close()
            if not conn is None:
                conn.close()

        return result
