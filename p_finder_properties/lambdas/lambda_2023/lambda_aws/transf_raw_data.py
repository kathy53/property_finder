import json
import boto3
import re
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
    agency = ', '.join(map(str,document.xpath('//div[@class="agency"]/div[@class="agency__info"]/span[@data-test="agency-name"]//text()'))) or None
    publisher = document.xpath('//div[@class="publisher"]/a/text()') or None
    publication_date = re.search('(.*?)\s-',document.xpath('//div[@class="date"]//text()')[0]).group(1) or None
    publisher_url = ', '.join(map(str,document.xpath('//div[@class="publisher"]/a/@href'))) or None
    agency_url = ', '.join(map(str,document.xpath('//div[@class="agency"]/div[@class="agency__info"]/a/@href'))) or None
    publisher_phone = ', '.join(map(str,document.xpath('//div[@class="phone-number"]/span/text()'))) or None

    surroundings = ', '.join(map(str,document.xpath('//div[@class="nearby-locations"]/ul//text()')))

    property_parameters = {
                  'source' : "lamudi",
                   'title' : document.xpath('//div[@class="main-title"]/h1/text()')[0],
             'property_url': re.search('adUrl:\s"(.*?)"',str(document.xpath('//script[contains(text(),"coordinates")]//text()')[0])).group(1),
                'location' : document.xpath('//div[@class="view-map__text"]/text()')[0],
             'description' : document.xpath('//div[@id="description-text"]/text()')[0],
               'raw_price' : document.xpath('//div[@class="prices-and-fees__price"]/text()')[0],
                   'price' : re.search('(\d.*?)MXN',str(document.xpath('//div[@class="prices-and-fees__price"]/text()')[0])).group(0).replace(' MXN','').replace(',',''),
                    'coin' : re.search('([A-Z]{1,})',str(document.xpath('//div[@class="prices-and-fees__price"]/text()')[0])).group(0),
            'details_item' : ', '.join(map(str,[ x for x in document.xpath('//div[@class="details-item"]//text()') if '\n' not in x ])),
          'place_features' : ', '.join(map(str,document.xpath('//div[@class="place-features"]//span//text()'))),
              'facilities' : ', '.join(map(str,document.xpath('//div[@class="facilities__item"]//text()'))),
               'image_url' : document.xpath('//div[@class="photos"]//img/@src')[0],
                'latitude' : re.search('latitude:\s"(\d{1,}.\d{1,})',str(document.xpath('//script[contains(text(),"coordinates")]//text()')[0])).group(1),
               'longitude' : re.search('longitude:\s"(-\d{1,}.\d{1,})',str(document.xpath('//script[contains(text(),"coordinates")]//text()')[0])).group(1),
                'province' : re.search('province:\s"(.*?)"',str(document.xpath('//script[contains(text(),"coordinates")]//text()')[0])).group(1),
                'locality' : re.search('locality:\s"(.*?)"',str(document.xpath('//script[contains(text(),"coordinates")]//text()')[0])).group(1),
                'district' : re.search('district:\s"(.*?)"',str(document.xpath('//script[contains(text(),"coordinates")]//text()')[0])).group(1),
                 'address' : re.search('address:\s["`](.*?)["`]',str(document.xpath('//script[contains(text(),"coordinates")]//text()')[0])).group(1),
            'surroundings' : surroundings,
               'publisher' : publisher,
                  'agency' : agency,
        'publication_date' : publication_date,
           'publisher_url' : publisher_url,
              'agency_url' : agency_url,
           'publisher_phone' : publisher_phone,
           'crawling_date' : datetime.datetime.now().strftime("%Y_%m_%d")
    }
    json_object = json.dumps(property_parameters, indent = 4, ensure_ascii=False) 

    
    prefix= datetime.datetime.now().strftime("%Y_%m_%d")
    file_name = f"/{property_parameters['property_url'][26:-5]}.json"
    s3.upload_fileobj(io.BytesIO(json_object.encode("utf-8")), Bucket=bucket, Key='processed/jsons/'+prefix+file_name) 
    print(file_name)