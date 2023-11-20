import json
import os
import io
import boto3
import pymysql
# from xmltodict import parse 
import hashlib
import logging #used to print your own logs

logger = logging.getLogger() #loggers should be instantiated trough the logging.getLogger(name)
logger.setLevel(logging.INFO) #logger threshold to process the logg

#DB credentials 
rds_host = os.environ["DB_HOST"]
name = os.environ["DB_USER"]
password = os.environ["DB_PASSWORD"]
db_name = os.environ["DB_NAME"]

def get_connection():
    """"
    Connecting with the database, timeout of 5 seg
    """
    try:
        conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        ssy.exit()
    return conn

def execute_query(conn, query):
    max_tries = 5
    try_number = 0
    while not conn.open and try_number < max_tries:
        logger.info("Reconnecting to database . . .")
        conn = get_connection()
        try_number += 1
    if try_number > 0:
        logger.info("Now connected!")
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()

conn = get_connection()

# s3 = boto3.client(
#     service_name='s3', 
#     region_name='us-west-2',
#     aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
#     aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
#     )

# s3 = boto3.client('s3')
# bucket = 'property-finder-data' 
# key ="processed/jsons/2023_11_09/detalle/41032-73-eb63892b2c77-fe12-686d362c-a298.json"
with open("41032-73-b088ad70dadf-4e78-a3d125a0-9bc9.json", "r") as f:
    contents = f.read()
try:
    #response = s3.get_object(Bucket=bucket, Key=key)
    #contents = response['Body'].read().decode("utf-8")
    contents = contents.replace('\n', '')
    contents = json.loads(contents)          #convert it into a dictionary
    
except Exception as e:
    print(e)
    print('Error hehehe')
    raise e
#Adding to real_estate_entity table 
pub = contents["agency"][0] or contents["publisher"][0]
encoded_pub = pub.encode()
object_pub = hashlib.sha1(encoded_pub)
publisher_id = object_pub.hexdigest()

publishers_keys= ['publisher_id', 'publisher', 'agency', 'publisher_url', 'agency_url', 'publisher_phone']
pub_values = [ contents[value] for value in publishers_keys[1:]]
pub_values.insert(0, publisher_id)
publishers_k = ', '.join([str(key) for key in publishers_keys])
publishers_v = '\', \''.join([str(value) for value in pub_values])

query = f"INSERT INTO real_estate_entity ({publishers_k}) VALUES ('{publishers_v}')"
# execute_query(conn, query)

adv = contents["property_url"][0]
encoded_adv = adv.encode()
object_adv = hashlib.sha1(encoded_adv)
advertisement_id = object_adv.hexdigest()

advertisements_keys = ['advertisement_id', 'source', 'title', 'property_url', 'location', 'description', 'raw_price', 'price', 'coin', 'details_item', 'place_features', 'facilities', 'image_url', 'latitude', 'longitude', 'province', 'locality', 'district', 'address', 'surroundings', 'publication_date', 'crawling_date', 'publisher_id']
advertisements_values = [ contents[value] for value in advertisements_keys[1:-1] ]
advertisements_values.insert(0, advertisement_id)
advertisements_values.append(publisher_id)

advertisements_k = ', '.join([str(key) for key in advertisements_keys])
advertisements_v = '\', \''.join([str(value) for value in advertisements_values])

query = f"INSERT INTO advertisements ({advertisements_k}) VALUES ('{advertisements_v}')"
# execute_query(conn, query)
import pdb; pdb.set_trace()

# conn_k = conn_k = 'publisher_id' + ', ' + 'advertisement_id'
# conn_v = publisher_id + '\', \'' + advertisement_id
# query = f"INSERT INTO advertisements_real_estate_entity_connector ({conn_k}) VALUES ('{conn_v}')"
# execute_query(conn, query)