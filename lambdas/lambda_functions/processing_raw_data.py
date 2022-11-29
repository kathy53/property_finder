import json
import boto3
import urllib.parse
from xmltodict import parse
import datetime
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        #print("CONTENT TYPE: " + response['ContentType'])
        contents = response['Body'].read().decode("utf-8")
        contents = contents.replace('.webp">', '.webp"></img>').replace('.jpg">', '.jpg"></img>')
        document = parse(contents)
        #return document
    except Exception as e:
        print(e)
        print('Error hehehe')
        raise e
   
    replace_characters =["\n.", "\n"]
    for c in replace_characters:
        description = document["div"].get('a', {}).get('div', [None])[1].get('#text').replace("\n\n", " ").replace(c, " ").replace("'", "")
        
    property_parameters = {
                    'title': document["div"].get('a', {}).get('@title'),
             'property_url': document["div"].get('a')get('@href'),
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
               'furnished' : bool(furnish) if (furnish := document["div"].get('@data-furnished')) else None,
              'year_built' : document["div"].get('@data-year_built'),
               'geo_point' : json.loads(document["div"].get('@data-geo-point')),
               'image_url' : document["div"].get('div', {}).get('div', {}).get('div', [{}]*3)[2].get('div', {}).get('a', {}).get('div', [{}])[0].get('img', {}).get('@data-src'),  
                  'source' : "lamudi",
              'agent_name' : document["div"].get('div', {}).get('div', {}).get('div', [{}]*3)[2].get('div', {}).get('a', {}).get('div', [{}]*2)[1].get('div', [{}])[0].get('#text'),
        'agent_membership' : document["div"].get('div', {}).get('div', {}).get('div', [{}]*3)[2].get('div', {}).get('a', {}).get('div', [{}])[1].get('div', [{}]*2)[1].get('#text'),            
               'agent_url' : document["div"].get('div', {}).get('div', {}).get('div', [{}]*3)[2].get('div', {}).get('a', {}).get('@href'),
           'crawling_date' : datetime.datetime.now().strftime("%Y_%m_%d")
    }
    
    json_object = json.dumps(property_parameters, indent = 4)
   
    prefix= datetime.datetime.now().strftime("%Y_%m_%d")
    file_name = f"/{property_parameters['property_url'][26:-5]}.json"
    s3.upload_fileobj(io.BytesIO(json_object.encode("utf-8")), Bucket=bucket, Key='processed/jsons/'+prefix+file_name)
    print(file_name)