from flask import json
import redis
from database.db_functions import get_beacons
from database.redis_functions import set_beacons


def beacon_cache(conn, cursor, redis_pool):
    result = {}
    beacons = get_beacons(conn, cursor)

    result['result'] = 0
    result['beacons'] = beacons

    r = redis.Redis(connection_pool=redis_pool)

    set_beacons(r, beacons)

    return True
