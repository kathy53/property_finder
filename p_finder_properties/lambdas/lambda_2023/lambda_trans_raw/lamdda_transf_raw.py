import json
import boto3
import urllib.parse
from lxml import etree
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
        #contents = contents.replace('.webp">', '.webp"></img>').replace('.jpg">', '.jpg"></img>')
        # print(contents)
        document =etree.HTML(contents)
        print(document)
    except Exception as e:
        print(e)
        print('Error hehehe')
        raise e
    
    #replace_characters =["\n.", "\n"]
    #for c in replace_characters:
     #   description = document["div"].get('a', {}).get('div', [None])[1].get('#text').replace("\n\n", " ").replace(c, " ").replace("'", "")
    
    property_parameters = {
                    'title': document.xpath('//div[@class="main-title"]/h1/text()')[0],
             'property_url': document.xpath('//div[@class="link"]/text()')[0],
                'location' : document.xpath('//div[@class="view-map__text"]/text()')[0],
            'details-item' : document.xpath('//div[@class="details-item"]//text()'),
          'place_features' : document.xpath('//div[@class="place-features"]//span//text()'),
                   'price' : document.xpath('//div[@class="prices-and-fees__price"]/text()')[0],
             'description' : document.xpath('//div[@id="description-text"]/text()')[0],   
              'facilities' : document.xpath('//div[@class="facilities__item"]//text()'),
                #here in the future could be used a try/"exeption" if the last element doesn't exist
                'latitude' : json.loads(document.xpath('//script[@type="application/ld+json"]//text()')[0])['@graph'][1]['geo']['latitude'],
               'longitude' : json.loads(document.xpath('//script[@type="application/ld+json"]//text()')[0])['@graph'][1]['geo']['longitude'],
               
               'image_url' : document["div"].get('div', {}).get('div', {}).get('div', [{}]*3)[2].get('div', {}).get('a', {}).get('div', [{}])[0].get('img', {}).get('@data-src'),  
                  'source' : document["div"].get('a', {}).get('@href', "").split(".")[1],
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