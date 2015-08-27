from flask import json
import redis
from database.db_functions import get_beacons, get_users
from database.redis_functions import set_beacons, set_user_names


def beacon_cache(conn, cursor, redis_pool):
    beacons = get_beacons(conn, cursor)

    r = redis.Redis(connection_pool=redis_pool)

    set_beacons(r, beacons)

    return True


def user_cache(conn, cursor, redis_pool):
    users = get_users(conn, cursor)

    r = redis.Redis(connection_pool=redis_pool)

    set_user_names(r, users)

    return True
