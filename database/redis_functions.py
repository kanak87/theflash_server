from datetime import datetime

redis_position_key = 'user_pos'
redis_beacon_key = 'beacon_list'
redis_user_name_key = 'user_name'


def set_user_name(r, user_id, user_name):
    return r.hset(redis_user_name_key, user_id, user_name)


def get_user_name(r, user_id):
    return r.hget(redis_user_name_key, user_id)


def get_users(r):
    users = []
    result = r.hgetall(redis_position_key)

    for user_pair in result.items():
        values = user_pair[1].split('/')
        users.append((user_pair[0], int(values[0]), int(values[1]), values[2],
                      datetime.strptime(values[3], "%Y-%m-%d %H:%M:%S.%f")))

    return users


def insert_user(r, user_id, beacon_id, user_name, distance):
    insert_value = "%d/%d/%s/%s" % (beacon_id, distance, user_name, datetime.now())
    return r.hset(redis_position_key, user_id, insert_value)


def remove_users(r, user_ids):
    p = r.pipeline()

    for user_id in user_ids:
        p.hdel(redis_position_key, user_id)

    p.execute()

    return True


def get_beacons(r):
    beacons = []
    result = r.hgetall(redis_beacon_key)

    for beacon_pair in result.items():
        values = beacon_pair[1].split('/')
        beacons.append((beacon_pair[0], values[0], values[1], int(values[2]), int(values[3])));

    return beacons


def insert_beacon(r, beacon_id, mac_addr, advertising_data, x, y):
    insert_value = "%s/%s/%d/%d" % (mac_addr, advertising_data, x, y)
    return r.hset(redis_beacon_key, beacon_id, insert_value)


def remove_beacon(r, beacon_id):
    return r.hdel(redis_beacon_key, beacon_id)


def set_beacons(r, beacons):
    r.delete(redis_beacon_key)

    if len(beacons) is 0:
        return 0

    beacon_map = {}
    for beacon in beacons:
        insert_value = "%s/%s/%d/%d" % (beacon['mac_addr'], beacon['advertising_data'], beacon['x'], beacon['y'])
        beacon_map[beacon['beacon_id']] = insert_value

    return r.hmset(redis_beacon_key, beacon_map)
