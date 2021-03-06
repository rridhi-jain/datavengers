# username - postgres
# password - xQw82gWFmCL9SfkDmdqy

from datetime import date
import sys
import logging
import psycopg2
import helper
import json

#rds settings
rds_host  = 'marsnest.cqjxjq7sdnq5.us-east-1.rds.amazonaws.com'
name = 'postgres'
password = 'xQw82gWFmCL9SfkDmdqy'
db_name = 'marsnest'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
  connection = psycopg2.connect(host = rds_host, port = 5432, user = name, password = password)
  cursor=connection.cursor()
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

# def drop_table():
#   with connection.cursor() as cur:
#     cur.execute("""drop table user_applications""")
#   connection.commit()
#   return True

# def create_user_table():
#   with connection.cursor() as cur:
#     cur.execute("""create table if not exists users (id SERIAL PRIMARY KEY not null, name varchar(255), email varchar(50) not null UNIQUE, mobile varchar(255), password varchar(255), role varchar(50), token varchar(255), dob date, created_at timestamp not null)""")
#   connection.commit()
#   return True

# def create_table():
#   with connection.cursor() as cur:
    # cur.execute("""create table if not exists user_applications (id SERIAL PRIMARY KEY not null, user_id int, uin varchar(10) not null, height int, weight int, blood_group varchar(5), diseases varchar(255), about varchar(255), qualification varchar(255), status varchar(255) not null, start_date date not null, end_date date not null, address_text varchar(255), country varchar(255), city varchar(255), state varchar(255), pincode varchar(255), created_at timestamp not null,CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id))""")
#   connection.commit()
#   return True

def create_user_applicaitons(user_application_obj):
  response = "Null"
  try:
    with connection.cursor() as cur:
      print("Execute Query")
      query = "INSERT INTO user_applications (user_id, uin, height, weight, blood_group, diseases, about, qualification, status, start_date, end_date, address_text, country, city, state, pincode, created_at) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
      print("---------")
      print(user_application_obj)
      print("---------")
      print(query)
      print("INSERT INTO user_applications (user_id, uin, height, weight, blood_group, diseases, about, qualification, status, start_date, end_date, address_text, country, city, state, pincode, created_at) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (user_application_obj.get('user_id'), user_application_obj.get('uin'), user_application_obj.get('height'), user_application_obj.get('weight'), user_application_obj.get('blood_group'), user_application_obj.get('diseases'), user_application_obj.get('about'), user_application_obj.get('qualification'), user_application_obj.get('status'), user_application_obj.get('start_date'),user_application_obj.get('end_date'),user_application_obj.get('address_text'),user_application_obj.get('country'),user_application_obj.get('city'),user_application_obj.get('state'),user_application_obj.get('pincode'),user_application_obj.get('created_at')))

      cur.execute("""INSERT INTO user_applications (user_id, uin, height, weight, blood_group, diseases, about, qualification, status, start_date, end_date, address_text, country, city, state, pincode, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (user_application_obj.get('user_id'), user_application_obj.get('uin'), user_application_obj.get('height'), user_application_obj.get('weight'), user_application_obj.get('blood_group'), user_application_obj.get('diseases'), user_application_obj.get('about'), user_application_obj.get('qualification'), user_application_obj.get('status'), user_application_obj.get('start_date'),user_application_obj.get('end_date'),user_application_obj.get('address_text'),user_application_obj.get('country'),user_application_obj.get('city'),user_application_obj.get('state'),user_application_obj.get('pincode'),user_application_obj.get('created_at')))
      print("---------")
      response = "Application Submitted Successfully"
  except Exception as err:
    print(err)
  finally:
    connection.commit()
  return response

def show_user_applications(user_email):
  response = "Null"
  results = []
  with connection.cursor() as cur:
    print("Select Query")
    query = f"SELECT user_applications.id, user_id, uin, height, weight, blood_group, diseases, about, qualification, status, start_date, end_date, user_applications.created_at, name as user_name, email as user_email, dob as user_dob FROM user_applications JOIN users ON user_id = users.id WHERE email = '{user_email}' Order By user_applications.created_at desc, user_applications.id desc LIMIT 1"
    print(query)
    cur.execute(query)
    response = cur.fetchall()
    results = helper.format_response(response)
  connection.commit()
  return results

def show_all_applications():
  response = "Null"
  results = []
  with connection.cursor() as cur:
    print("Select Query")
    query = f"SELECT user_applications.id, user_id, uin, height, weight, blood_group, diseases, about, qualification, status, start_date, end_date, user_applications.created_at, name as user_name, email as user_email, dob as user_dob FROM user_applications JOIN users ON user_id = users.id"
    cur.execute(query)
    response = cur.fetchall()
    results = helper.format_response(response)
  connection.commit()
  return results

def get_user_application(user_application_id):
  response = "Null"
  results = []
  with connection.cursor() as cur:
    print("Select Query")
    query = f"SELECT user_applications.id, user_id, uin, height, weight, blood_group, diseases, about, qualification, status, start_date, end_date, user_applications.created_at, name as user_name, email as user_email, dob as user_dob FROM user_applications JOIN users ON user_id = users.id WHERE user_applications.id = {user_application_id}"
    cur.execute(query)
    response = cur.fetchall()
    results = helper.format_response(response)
  connection.commit()
  return results

def create_user(user_obj):
  response = "Null"
  try:
    with connection.cursor() as cur:
      print("Execute Query")
      query = "INSERT INTO users (name, email, mobile, role, dob, token, created_at) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (user_obj.get('name'), user_obj.get('email'), user_obj.get('mobile'), user_obj.get('role'), user_obj.get('dob'), user_obj.get('token'), user_obj.get('created_at'))
      print("---------")
      print(query)
      cur.execute("""INSERT INTO users (name, email, mobile, role, dob, token, created_at) VALUES (%s, %s, %s, %s, %s, %s)""",(user_obj.get('name'), user_obj.get('email'), user_obj.get('mobile'), user_obj.get('role'), user_obj.get('dob'),user_obj.get('token'), user_obj.get('created_at')))
      response = "User Created Successfully"
      print(response)
  except Exception as err:
    print(err)
  finally:
    connection.commit()
  return response

def get_user_by_id(user_id):
  response = "Null"
  results = []
  with connection.cursor() as cur:
    print("Select Query")
    query = f"SELECT id, name, email, dob, mobile, token, role, created_at FROM users WHERE id = {user_id}"
    cur.execute(query)
    response = cur.fetchall()
    results = helper.format_user_response(response)
  connection.commit()
  return results

def get_user_by_email(user_email):
  response = "Null"
  results = []
  with connection.cursor() as cur:
    print("Select Query")
    query = "SELECT id, name, email, dob, mobile, token, role, created_at FROM users WHERE email = '%s'" % user_email
    print(query)
    print(user_email)
    cur.execute(query)
    response = cur.fetchall()
    results = helper.format_user_response(response)
  connection.commit()
  return results

def update_user(user_obj):
  response = "Null"
  with connection.cursor() as cur:
    print("Execute Query")
    query = "UPDATE users SET token = %s, mobile = %s, dob = %s WHERE email = %s"
    print("---------")
    print(query)
    cur.execute("""UPDATE users SET token = %s, mobile = %s, dob = %s WHERE email = %s""", (user_obj.get('token'), user_obj.get('mobile'), user_obj.get('dob'), user_obj.get('email')))
    response = "User updated Successfully"
  connection.commit()
  return response