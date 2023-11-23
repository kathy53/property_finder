"""
Fetching historical information about air quality, sun radiation and weather for a given Mexican municipality
"""
import requests
# !pip install pymysql
import pymysql
import logging
import os
import pandas as pd
from unidecode import unidecode
from p_finder_weather.settings import states_municipalities_centroids

# finding the municipios from the table "advertisements"
# connecting with the database
logger = logging.getLogger()  #loggers should be instantiated trough the logging.getLogger(name)
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
        # datasets = cur.fetchall()
        conn.commit()
    # return datasets

def get_json(url):
    url = url
    response = requests.get(url)
    json_data = response.json()
    return json_data

conn = get_connection()

try:
    query = f"SELECT province, locality FROM advertisements"
    db_loc = pd.read_sql(query, get_connection())
    #db_localities = execute_query(conn, query)
    db_localities = list(zip(db_loc.province, db_loc.locality))
    unique_localities = set(db_localities)
except Exception as e:
    print(e)
    print('Error hehehe')
    raise e

environtment = pd.DataFrame()
latitudes = []
longitudes = []
states = []
localities = []

distinct_loc_in_file = [loc for sub_dict in states_municipalities_centroids.values() for loc in sub_dict.keys()]
distinct_loc_in_file = [loc for loc in distinct_loc_in_file if distinct_loc_in_file.count(loc) == 1]

for state, locality in unique_localities:
    state = unidecode(state).lower().replace(" ","_")
    locality = unidecode(locality).lower().replace(" ","_")

    # Here it could be some mistakes because some times names could be mixed
    if any(locality in loc for loc in states_municipalities_centroids[state].keys()):                                               # validating existing location 
        validated_loc = [locality in loc for loc in states_municipalities_centroids[state].keys()]                          
        locality = next((key for key, flag in zip(states_municipalities_centroids[state].keys(), validated_loc) if flag), None)     # updating locality to an existing one in the local states_municipalities.json file
        if state:
            coordinates = states_municipalities_centroids[state][locality]
            states.append(state)
            localities.append(locality)
            
            latitudes.append(coordinates[0])
            longitudes.append(coordinates[1])

        else:
            if locality in distinct_loc_in_file:
                state = [state for state, sub_dict in states_municipalities_centroids.items() if locality in sub_dict.keys()]
                coordinates = states_municipalities_centroids[state][locality]
                states.append(state)
                localities.append(locality)
                latitudes.append(coordinates[0])
                longitudes.append(coordinates[1])
            else:
                state = "unknown"
                with open ("missing_localities.txt", "a") as f:
                    text = state + ': ' + locality + '\n'
                    f.write(text)
    # in case the locality does not exist in the advertisement table 
    else:                                                                                              
        with open ("missing_localities.txt", "a") as f:
            text = state + ': ' + locality + '\n'
            f.write(text)

environtment["states"] = states
environtment["localities"] = localities
environtment["latitude_centroid"] = latitudes
environtment["longitude_centroid"] = longitudes

latitudes_probe = latitudes[:3]
longitudes_probe = longitudes[:3]

latitude = ','.join([str(lat) for lat in latitudes_probe])
longitude = ','.join([str(lon) for lon in longitudes_probe])

aq_and_sr_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={latitude}&longitude={longitude}&hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,aerosol_optical_depth,dust,uv_index,uv_index_clear_sky&start_date=2022-08-01&end_date=2023-11-20"
weath_url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date=2020-01-01&end_date=2023-11-20&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,precipitation,rain,snowfall,snow_depth,weather_code,cloud_cover,et0_fao_evapotranspiration,wind_speed_10m,wind_direction_10m,wind_gusts_10m,soil_temperature_0_to_7cm"

aq_and_sr_json = get_json(aq_and_sr_url)
weath_json = get_json(weath_url)
import pdb; pdb.set_trace()

aq_cols = ['time', 'pm10', 'pm2_5', 'carbon_monoxide', 'nitrogen_dioxide', 'sulphur_dioxide', 'ozone', 'aerosol_optical_depth', 'dust']
sr_cols = ['time', 'uv_index', 'uv_index_clear_sky']
wt_cols = ['time', 'temperature_2m','relative_humidity_2m','dew_point_2m','apparent_temperature','precipitation','rain','snowfall','snow_depth','weather_code','cloud_cover','et0_fao_evapotranspiration','wind_speed_10m','wind_direction_10m','wind_gusts_10m','soil_temperature_0_to_7cm']

env_temp = pd.DataFrame(aq_and_sr_json)
env_temp["aq"] = env_temp["hourly"].map(lambda x: {key: x[key] for key in aq_cols})
env_temp["sr"] = env_temp.hourly.map(lambda x: {key: x[key] for key in sr_cols})
#selection
environtment = pd.concat([environtment, env_temp], axis=1)

cols = ['states', 'localities', 'latitude_centroid', 'longitude_centroid', 'latitude', 'longitude', 'aq', 'sr']
cols_s = ', '.join(map(str,cols))
for _, row in environtment.iloc[:3].iterrows():
    values = '\', \''.join(map(str,row[[cols]].tolist()))
    query = f"INSERT INTO environtments ({cols_s}) VALUES('{values}')"
    print(query)
    # execute_query(conn, query)
