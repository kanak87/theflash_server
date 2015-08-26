import os

db_user_name = 'theflash'
db_password = '1234'
db_name = 'theflash'
db_host = 'localhost'

redis_host = 'localhost'
redis_port = 6379

service_port = 14000

dir_path = os.path.dirname(__file__)

static_path = os.path.join(dir_path, 'static')
template_path = os.path.join(dir_path, 'templates')