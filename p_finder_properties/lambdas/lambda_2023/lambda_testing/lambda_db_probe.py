import json
import os
import io
import boto3
import pymysql
# from xmltodict import parse 
# import datetime
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

s3 = boto3.client(
    service_name='s3', 
    region_name='us-west-2',
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    )

s3 = boto3.client('s3')
bucket = 'property-finder-data' 
key ="processed/jsons/2022_11_22/3-recamaras-mod-136-casa-sustentable-en-privada-residencial.json"

try:
    response = s3.get_object(Bucket=bucket, Key=key)
    contents = response['Body'].read().decode("utf-8")
    contents = contents.replace('.webp">', '.webp"></img>').replace('.jpg">', '.jpg"></img>')
    contents = json.loads(contents)          #convert it into a dictionary
    #join([str(value) for value in nomina.dict().values()])
    keys = ', '.join([str(key) for key in contents.keys()])
    values = '\',\''.join([str(value) for value in contents.values()])
except Exception as e:
    print(e)
    print('Error hehehe')
    raise e

#advertisements_dict ={key:contents[key] for key in contents if key not in ["agent_name", "agent_membership", "agent_url", "crawling_date"]}

query = f"INSERT INTO advertisements ({keys}) VALUES ('{values}')"

#print(query)
execute_query(conn, query)

