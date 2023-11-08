""" Crawler to fetch property data from the website lamudi.com.mx/yucatan/casa/for-sale/ 

    Fetching a list, for each listed property in lamudi-yucatan. Properties' data: geo-point, 
    property name, town, description, price, area in square meters, buil square meters, and
    bed rooms
    The adds are showed in batchs of 30. 
    Store the info in an individual file and upload it into 'property-finder-data' s3-bucket

"""

from gc import callbacks
from pickle import NONE
import scrapy   
import pdb     
from math import ceil
import re      
import os
import boto3
import io
import datetime

from p_finder_scrapper.spiders.settings import mexican_states

class PropertiesSpider(scrapy.Spider):  
    """ name is used as a reference of this code (spider) for scrapy commands
            such as 'scrapy crawl "name" '== instruction to run the spider
        allowed_domains is a safety feature that restrict the spider to crawling the given domain
            it allows to avoid accidental errors
        start_urls is the starting point 
        """
    name = 'properties_crawler'     
    BUCKET = 'property-finder-data'            
    s3 = boto3.client(service_name='s3', region_name='us-west-2',
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    )
    allowed_domains = ['www.lamudi.com.mx']
    #creo que tengo que cambiar los siguientes parametros
    custom_settings= {
        'AUTOTHROTTLE_START_DELAY': 3,
        'AUTOTHROTTLE_MAX_DELAY': 15.0,
        'CONCURRENT_REQUEST_PER_DOMAIN': 1,
        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUEST_PER_IP':1,
        'ROBOTSTXT_OBEY': False
        }
    
    start_urls = ["https://www.lamudi.com.mx/"+ state +"/casa/for-sale/" for state in mexican_states["states"] ]
    #The next list is to do some tests, but for the final code use the above list
    start_urls = start_urls[3:5]
    
    #def __init__(self):
    
    def parse(self, response):
        """Here the scrapy spider works by connecting to each "start_urls"
        We are going to create a list of all the pages that show houses for each state, the first page show 30 properties
        At the bottom of the first page we can find data pagination
        """
        #Fetching the total number of pages if all properties for a given state are required
        #pagination = response.xpath('//div[@class="pagination"]//div[@class="sort-text"]/text()').getall()
        #number_of_pages = re.search('\d{2,}', pagination[0]).group()
        #number_of_pages = response.xpath('//select[@class="sorting nativeDropdown js-pagination-dropdown"]/@data-pagination-end').getall()
        #list of all links-categories
        #list_link_pages=['https://www.lamudi.com.mx/yucatan/casa/for-sale/?page=' + str(l) for l in range(1, int(number_of_pages))] 
        
        #url list, cosidering only two pages for each Mexican state
        number_page = ["?page=1", "?page=2"]
        url_string = response.url
        list_link_pages = [ url_string + pagination for pagination in number_page]
                
        for url_n in list_link_pages:
            #doing the request for each url
            yield scrapy.Request(url_n, callback=self.parse_pages_list)
            #for a given url_n it calls (callback) the function parse_pages_list and get the response of parse_pages_list
        
    def parse_pages_list(self, response): 
        """ Request a 'url_n' to gather url of the listed properties on the given 'url_n'    
        """
        list_property_url = response.xpath('//div[@id="listings"]//a/@href').getall()
        list_property_url = [url for url in list_property_url if "detalle" in url]
        list_property_urls = ["https://www.lamudi.com.mx" + url for url in list_property_url]

        for url in list_property_urls:
            yield scrapy.Request(url, callback=self.parse_house_page)

    def parse_house_page(self, response): 
        """ Request a 'url' to gather detailed info about the property on the given 'url'    
            Store property information into a specific AWS object        
        """
        def store_in_s3(file_name, property_info):
            """Storing data for each property in an individual object
            The name of the file should be unique to serve as a validation for future crawlings
            """
            # Storing data locally
            # file_name = "./../properties_data/{}".format(file_name[34:])
            # with open(file_name, 'w') as f:
            #     f.write(property_info)
            
            # Uploading files into S3 bucket
            prefix= datetime.datetime.now().strftime("%Y_%m_%d")
            file_name = "/{}".format(file_name[34:])
            self.s3.upload_fileobj(io.BytesIO(property_info.encode("utf-8")), self.BUCKET, 'sources/lamudi/all_mexico/'+prefix+file_name)    

        geocoordinates = response.xpath('//head/script[@type="application/ld+json"]').getall()

        row_details = response.xpath('//div[@class="row-details"]').getall()
        description = response.xpath('//div[@class="description"]').getall()
        facilities = response.xpath('//div[@class="facilities"]').getall()
        geo_data =  response.xpath('//head/script[@type="application/ld+json"]').getall()
        all_property_info = row_details[0] + description[0] + facilities[0] + geo_data[0]

        property_url = response.url
        pdb.set_trace()

        #write the files
        store_in_s3(property_url, all_property_info)
        
        print('\n\n+++++++++++++++++++++++++++++++++++\nFinishing one property :)\n\n+++++++++++++++++++++++++++++++++++\n')
    