def add_new_user(user_name, social_id, conn, cursor):
    result = False

    queryResult = cursor.execute(
        "insert into user (user_name, social_id, registration_time) values('%s', '%s', now())" % (
        user_name, social_id))
    conn.commit()
    result_data = cursor.fetchone()

    if not (result_data is None and cursor.rowcount >= 1):
        raise Exception("db error, insert new user")
    else:
        result = True

    return result


def get_user_id(user_name, social_id, conn, cursor, exception_eanble = True):
    user_id = None

    queryResult = cursor.execute(
        "select user_id from user where user_name='%s' and social_id='%s'" % (user_name, social_id))
    result_data = cursor.fetchone()

    if result_data is None or cursor.rowcount == 0:
        if exception_eanble is True:
            raise Exception("db error, select new user")
    else:
        user_id = int(result_data[0])

    return user_id