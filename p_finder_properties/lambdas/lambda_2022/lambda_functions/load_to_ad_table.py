import json
import urllib.parse
import os
import io
import boto3
import pymysql
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
        contents = contents.replace('.webp">', '.webp"></img>').replace('.jpg">', '.jpg"></img>')
        contents = json.loads(contents)          #convert it into a dictionary
        keys = ', '.join([str(key) for key in contents.keys()])
        values = '\',\''.join([str(value) for value in contents.values()])
    except Exception as e:
        print(e)
        print('Error hehehe')
        raise e
    query = f"INSERT INTO advertisements ({keys}) VALUES ('{values}')"
    #print(query)
    execute_query(conn, query)