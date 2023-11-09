import json
import os
import io
import boto3
from lxml import etree 
import datetime
import re

s3 = boto3.client(service_name='s3', region_name='us-west-2',
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    )
#S3 event triggers  the lambda
s3 = boto3.client('s3')
bucket = 'property-finder-data' 
key ="sources/lamudi/all_mexico/2023_11_09/41032-73-eb63892b2c77-fe12-686d362c-a298-34d6"
    
property_parameters = []

try:
    response = s3.get_object(Bucket=bucket, Key=key)
    contents = response['Body'].read().decode("utf-8")
    #contents = contents.replace('.webp">', '.webp"></img>').replace('.jpg">', '.jpg"></img>')
    document =etree.HTML(contents)
    print(document)
except Exception as e:
    print(e)
    print('Error hehehe')
    raise e

replace_characters =["\n.", "\n"]
import pdb; pdb.set_trace()

# for c in replace_characters:
#     description = document["div"].get('a', {}).get('div', [None])[1].get('#text').replace("\n\n", " ").replace(c, "")
agency = document.xpath('//div[@class="agency"]/div[@class="agency__info"]/span[@data-test="agency-name"]//text()')
agency = agency or document.xpath('//div[@class="publisher"]/a/text()')

publication_date = re.search('(.*?)\s-',document.xpath('//div[@class="date"]//text()')[0]).group(1)

publisher_url = document.xpath('//div[@class="publisher"]/a/@href')
publisher_url = publisher_url or document.xpath('//div[@class="agency"]/div[@class="agency__info"]/a/@href')

publisher_phone = document.xpath('//div[@class="phone-number"]/span/text()')

surroundings = document.xpath('//div[@class="nearby-locations"]/ul//text()')

property_parameters = {
                    'title': document.xpath('//div[@class="main-title"]/h1/text()')[0],
             'property_url': re.search('adUrl:\s"(.*?)"',str(document.xpath('//script[contains(text(),"coordinates")]//text()')[0])).group(1),
                'location' : document.xpath('//div[@class="view-map__text"]/text()')[0],
             'description' : document.xpath('//div[@id="description-text"]/text()')[0],
               'raw_price' : document.xpath('//div[@class="prices-and-fees__price"]/text()')[0],
                   'price' : re.search('(\d.*?)MXN',str(document.xpath('//div[@class="prices-and-fees__price"]/text()')[0])).group(0).replace(' MXN','').replace(',',''),
                    'coin' : re.search('([A-Z]{1,})',str(document.xpath('//div[@class="prices-and-fees__price"]/text()')[0])).group(0),
            'details_item' : [ x for x in document.xpath('//div[@class="details-item"]//text()') if '\n' not in x ],
          'place_features' : document.xpath('//div[@class="place-features"]//span//text()'),
              'facilities' : document.xpath('//div[@class="facilities__item"]//text()'),
               'image_url' : document.xpath('//div[@class="photos"]//img/@src')[0],
                'latitude' : re.search('latitude:\s"(\d{1,}.\d{1,})',str(document.xpath('//script[contains(text(),"coordinates")]//text()')[0])).group(1),
               'longitude' : re.search('longitude:\s"(-\d{1,}.\d{1,})',str(document.xpath('//script[contains(text(),"coordinates")]//text()')[0])).group(1),
                'province' : re.search('province:\s"(.*?)"',str(document.xpath('//script[contains(text(),"coordinates")]//text()')[0])).group(1),
                'locality' : re.search('locality:\s"(.*?)"',str(document.xpath('//script[contains(text(),"coordinates")]//text()')[0])).group(1),
                'district' : re.search('district:\s"(.*?)"',str(document.xpath('//script[contains(text(),"coordinates")]//text()')[0])).group(1),
                 'address' : re.search('address:\s["`](.*?)["`]',str(document.xpath('//script[contains(text(),"coordinates")]//text()')[0])).group(1),
            'surroundings' : surroundings,
               'publisher' : agency,
        'publication_date' : publication_date,
           'publisher_url' : publisher_url,
           'publisher_phone' : publisher_phone,
           'crawling_date' : datetime.datetime.now().strftime("%Y_%m_%d")
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