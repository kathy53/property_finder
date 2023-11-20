import json
import urllib.parse
import os
import io
import boto3
import pymysql
import logging #used to print your own logs
import hashlib

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
        conn =pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
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
#############################

s3 = boto3.client('s3')

def lambda_handler(event, context):

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    logger.info(f'Current file to process: {key}')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        contents = response['Body'].read().decode("utf-8")
        contents = contents.replace('\n', '')
        contents = json.loads(contents)          #convert it into a dictionary
        #keys = ', '.join([str(key) for key in contents.keys()])
        #values = '\',\''.join([str(value) for value in contents.values()])
    except Exception as e:
        print(e)
        print('Error hehehe')
        raise e

    pub = contents["agency"][0] or contents["publisher"][0]
    encoded_pub = pub.encode()
    object_pub = hashlib.sha1(encoded_pub)
    publisher_id = object_pub.hexdigest()
    publishers_keys= ['publisher_id', 'publisher', 'agency', 'publisher_url', 'agency_url', 'publisher_phone']
    pub_values = [ contents[value] for value in publishers_keys[1:]]
    pub_values.insert(0, publisher_id)
    publishers_k = ', '.join([str(key) for key in publishers_keys])
    publishers_v = '\', \''.join([str(value) for value in pub_values])

    queryRE = f"INSERT INTO real_estate_entity ({publishers_k}) VALUES ('{publishers_v}') ON DUPLICATE KEY UPDATE publisher_id=publisher_id"
    execute_query(conn, queryRE)

    adv = contents["property_url"]
    encoded_adv = adv.encode()
    object_adv = hashlib.sha1(encoded_adv)
    advertisement_id = object_adv.hexdigest()
    advertisements_keys = ['advertisement_id', 'source', 'title', 'property_url', 'location', 'description', 'raw_price', 'price', 'coin', 'details_item', 'place_features', 'facilities', 'image_url', 'latitude', 'longitude', 'province', 'locality', 'district', 'address', 'surroundings', 'publication_date', 'crawling_date', 'publisher_id']
    advertisements_values = [ contents[value] for value in advertisements_keys[1:-1] ]
    advertisements_values.insert(0, advertisement_id)
    advertisements_values.append(publisher_id)
    advertisements_k = ', '.join([str(key) for key in advertisements_keys])
    advertisements_v = '\', \''.join([str(value) for value in advertisements_values])

    queryA = f"INSERT INTO advertisements ({advertisements_k}) VALUES ('{advertisements_v}') ON DUPLICATE KEY UPDATE advertisement_id=advertisement_id"
    execute_query(conn, queryA)

