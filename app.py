from flask import Flask, json
from flask.ext.mysql import MySQL
from datetime import timedelta, datetime
from redis import Redis
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import tornado.web
import time
import settings

app = Flask(__name__)
redis = Redis()
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = settings.db_user_name
app.config['MYSQL_DATABASE_PASSWORD'] = settings.db_password
app.config['MYSQL_DATABASE_DB'] = settings.db_name
app.config['MYSQL_DATABASE_HOST'] = settings.db_host

mysql.init_app(app)

class update_user_pos(tornado.web.RequestHandler):	
	def get(self):
		return self.post()

	def post(self):
		try:
			result = []

			user_id = self.get_argument('user_id')
			x = int(self.get_argument('x'))
			y = int(self.get_argument('y'))

			conn = mysql.connect()
			cursor = conn.cursor()

			queryResult = cursor.execute("replace into user (user_id, x, y, update_time) values('%s', %d, %d, now())" % (user_id, x, y))
			conn.commit()

			resultData = cursor.fetchone()
			
			if resultData == None and cursor.rowcount >= 1:
				result.append({'result' : 0})
			else:
				result.append({'result' : -1});
				result.append({'error_msg' : 'db replace error'});

		except Exception as e:
			print e
			result.append({'result' : -1});
			result.append({'error_msg' : 'db exception'});
		finally:
			cursor.close()
			conn.close()

		self.write(json.dumps(result))

class get_users(tornado.web.RequestHandler):
	def get(self):
		return self.post()

	def post(self):
		try:
			result = []

			conn = mysql.connect()
			cursor = conn.cursor()

			cursor.execute('select * from user')

			users = []
			expired_users = []

			columns = list([d[0] for d in cursor.description])
			columns.pop();

			nowTime = datetime.today();
			expireTimeDelta = timedelta(seconds=60);

			for row in cursor:
				if nowTime > row[3] + expireTimeDelta:
					expired_users.append(row[0])
					continue
				else:
					users.append(dict(zip(columns, row)))

			delete_users_query = ""
			
			if len(expired_users) > 0:
				delete_users_query = "delete from user where user_id in ("
				delete_users_query += "'" + expired_users[0] + "'"

				for expired_user_id in expired_users[1:]:
					delete_users_query += ",'" + expired_user_id + "'"

				delete_users_query += ")";

				print delete_users_query

				queryResult = cursor.execute(delete_users_query)
				conn.commit()

				resultData = cursor.fetchone()
				
				if resultData != None or cursor.rowcount < 1:
					raise Exception('delete queury error')

			result.append({'result' : 0});
			result.append({'users' : users})

		except Exception as e:
			print e
			result.append({'result' : -1});
			result.append({'error_msg' : 'db exception'});
		finally:
			cursor.close()
			conn.close()

		self.write(json.dumps(result))

class get_beacons(tornado.web.RequestHandler):
	def get(self):
		return self.post()

	def post(self):
		try:
			result = []

			conn = mysql.connect()
			cursor = conn.cursor()

			cursor.execute('select * from beacon')

			beacons = []

			columns = tuple([d[0] for d in cursor.description].pop())
			print columns

			for row in cursor:
				for elem in row:
					print elem
				beacons.append(dict(zip(columns, row)))
			result.append({'result' : 0});
			result.append({'beacons' : beacons})

		except Exception as e:
			print e
			result.append({'result' : -1});
			result.append({'error_msg' : 'db exception'});
		finally:
			cursor.close()
			conn.close()

		self.write(json.dumps(result))

class register_beacon(tornado.web.RequestHandler):
	def get(self):
		return self.post()

	def post(self):
		try:
			result = []

			mac_addr = self.get_argument('mac_addr')
			advertising_data = self.get_argument('ad_data')
			x = self.get_argument('x')
			y = self.get_argument('y')

			conn = mysql.connect()
			cursor = conn.cursor()

			queryResult = cursor.execute("insert into theflash.beacon (mac_addr, advertising_data, x, y) values('%s', '%s', %s, %s)" %
			 (mac_addr, advertising_data, x, y))
			conn.commit()

			resultData = cursor.fetchone()
			
			if resultData == None and cursor.rowcount == 1:
				result.append({'result' : 0})
			else:
				result.append({'result' : -1});
				result.append({'error_msg' : 'beacon insert error'});

		except Exception as e:
			print e
			if tuple(e)[0] == 1062:
				result.append({'result' : -1});
				result.append({'error_msg' : 'already registered beacon'});
			else:
				result.append({'result' : -1});
				result.append({'error_msg' : 'db exception'});

		finally:
			if not cursor is None:
				cursor.close()
			if not conn is None:
				conn.close()

		self.write(json.dumps(result))


class unregister_beacon(tornado.web.RequestHandler):
	def get(self):
		return self.post()

	def post(self):
		try:
			result = []

			mac_addr = self.get_argument('mac_addr')
			advertising_data = self.get_argument('ad_data')

			conn = mysql.connect()
			cursor = conn.cursor()

			queryResult = cursor.execute("delete from theflash.beacon where mac_addr='%s' and advertising_data='%s'" %
			 (mac_addr, advertising_data))
			conn.commit()

			resultData = cursor.fetchone()
			
			if resultData == None and cursor.rowcount == 1:
				result.append({'result' : 0})
			else:
				result.append({'result' : -1});
				result.append({'error_msg' : 'beacon delete error'});

		except Exception as e:
			print e
			result.append({'result' : -1});
			result.append({'error_msg' : 'db exception'});

		finally:
			cursor.close()
			conn.close()

		self.write(json.dumps(result))

if __name__ == "__main__":
	application = tornado.web.Application([
	        (r"/update_user_pos", update_user_pos),
	        (r"/get_users", get_users),
	        (r"/get_beacons", get_beacons),
	        (r"/register_beacon", register_beacon),
	        (r"/unreigster_beacon", unregister_beacon),
	        ])#,
	        #autoreload=True)
	        #debug=True)

	server = tornado.httpserver.HTTPServer(application)
	server.bind(14000)
	server.start(4)
	IOLoop.current().start()
