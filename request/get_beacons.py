from base_request import RequestBase
from database.redis_functions import get_beacons

beacon_columns = ['beacon_id', 'mac_addr', 'advertising_data', 'x', 'y']


class RequestGetBeacons(RequestBase):
    def process_data(self, data):
        result = {}
        try:
            r = self.get_redis_connection()
            beacon_dict = {}

            beacons = get_beacons(r)
            for beacon in beacons:
                beacon_dict = dict(zip(beacon_columns, beacon))

            result['result'] = 0
            result['beacons'] = beacon_dict

        except Exception as e:
            print e
            result['result'] = -1
            result['error_msg'] = str(e)

        return result
