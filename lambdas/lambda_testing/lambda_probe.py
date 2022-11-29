import json
import os
import io
import boto3
from xmltodict import parse 
import datetime

s3 = boto3.client(service_name='s3', region_name='us-west-2',
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    )

s3 = boto3.client('s3')
bucket = 'property-finder-data' 
key ="sources/lamudi/2022_11_22/3-recamaras-mod-136-casa-sustentable-en-privada-residencial.html"
    
property_parameters = []

try:
    response = s3.get_object(Bucket=bucket, Key=key)
    contents = response['Body'].read().decode("utf-8")
    contents = contents.replace('.webp">', '.webp"></img>').replace('.jpg">', '.jpg"></img>')
    document = parse(contents)
    #print(document)
except Exception as e:
    print(e)
    print('Error hehehe')
    raise e

replace_characters =["\n.", "\n"]
for c in replace_characters:
    description = document["div"].get('a', {}).get('div', [None])[1].get('#text').replace("\n\n", " ").replace(c, "")

property_parameters = {
                'title': document["div"].get('a', {}).get('@title'),
         'property_url': document["div"].get('a')['@href'],
            'location' : document['div'].get('a', {}).get('div', '[null]')[0].get('div', {}).get('span', [{}]*2)[1].get('#text'),
         'description' : description,
               'price' : document["div"].get('@data-price'),
            'category' : document["div"].get('@data-category'),
    #in json.loads() the s makes reference to the string
         'subcategory' : json.loads(document["div"].get('@data-subcategories', '[null]'))[-1],
            #here in the future could be used a try/"exeption" if the last element doesn't exist
            'bedrooms' : document["div"].get('@data-bedrooms'),
         'total_rooms' : document["div"].get('@data-rooms_total'),
          'car_spaces' : document["div"].get('@data-car_spaces'), 
           'bathrooms' : document["div"].get('@data-bathrooms'),
       'building_size' : document["div"].get('@data-building_size'),
           'land_size' : document["div"].get('@data-land_size'),
           'furnished' : document["div"].get('@data-furnished'),
          'year_built' : document["div"].get('@data-year_built'),
           'geo_point' : json.loads(document["div"].get('@data-geo-point')),
           'image_url' : document["div"].get('div', {}).get('div', {}).get('div', [{}]*3)[2].get('div', {}).get('a', {}).get('div', [{}])[0].get('img', {}).get('@data-src'),  
              'source' : document["div"].get('a', {}).get('@href', "").split(".")[1],
          'agent_name' : document["div"].get('div', {}).get('div', {}).get('div', [{}]*3)[2].get('div', {}).get('a', {}).get('div', [{}]*2)[1].get('div', [{}])[0].get('#text'),
    'agent_membership' : document["div"].get('div', {}).get('div', {}).get('div', [{}]*3)[2].get('div', {}).get('a', {}).get('div', [{}])[1].get('div', [{}]*2)[1].get('#text'),            
           'agent_url' : document["div"].get('div', {}).get('div', {}).get('div', [{}]*3)[2].get('div', {}).get('a', {}).get('@href')
}


print(property_parameters['property_url'])
########################################

json_object = json.dumps(property_parameters, indent = 4) 


prefix= datetime.datetime.now().strftime("%Y_%m_%d")
file_name = f"/{property_parameters['property_url'][-31:-5]}.json"
s3.upload_fileobj(io.BytesIO(json_object.encode("utf-8")), bucket, 'probe/jsons/'+prefix+file_name) 

###
#reviewing the buscket content
key = 'sources/lamudi/jsons/'+prefix+file_name
response2 = s3.get_object(Bucket=bucket, Key=key)
contents2 = response2['Body'].read().decode("utf-8")
print(contents2)