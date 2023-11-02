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
    start_urls = ['https://www.lamudi.com.mx/yucatan/casa/for-sale/']
    #def __init__(self):
    
    def parse(self, response):
        """Here the scrapy spider works by connecting to each "start_urls"
        We are going to create a list of all the pages that show houses, the first page show 30 properties
        At the bottom of the first page we can find data pagination
        """
        #Fetching the total number of pages
        #pdb.set_trace()
        #pagination = response.xpath('//div[@class="pagination"]//div[@class="sort-text"]/text()').getall()
        #number_of_pages = re.search('\d{2,}', pagination[0]).group()
        #number_of_pages = response.xpath('//select[@class="sorting nativeDropdown js-pagination-dropdown"]/@data-pagination-end').getall()
        #list of all links-categories
        #list_link_pages=['https://www.lamudi.com.mx/yucatan/casa/for-sale/?page=' + str(l) for l in range(1, int(number_of_pages))] 
        
        #The next list is to do some tests, but for the final code to use the above list_link_pages
        list_link_pages = ['https://www.lamudi.com.mx/yucatan/casa/for-sale/?page=1', "https://www.lamudi.com.mx/yucatan/casa/for-sale/?page=2"]
        for url_n in list_link_pages:
            #doing the request for each url
            yield scrapy.Request(url_n, callback=self.parse_pages_list)
            #for a given url_n it calls (callback) the function parse_pages_list and get the response of parse_pages_list
        
    
    def parse_pages_list(self, response): 
        """ Request a 'url_n' to gather detailed info about the listed properties on the given 'url_n'    
            Store property information into a specific AWS object        
        """
        def store_in_s3(file_name, property_info):
            """Storing data for each property in an individual object
            The name of the file should be unique to serve as a validation for future crawlings
            """
            # Storing data locally
            # file_name = "./../properties_data/{}".format(file_name[26:])
            # with open(file_name, 'w') as f:
            #     f.write(property_info)
            
            # Uploading files into S3 bucket
            prefix= datetime.datetime.now().strftime("%Y_%m_%d")
            file_name = "/{}".format(file_name[26:])
            self.s3.upload_fileobj(io.BytesIO(property_info.encode("utf-8")), self.BUCKET, 'sources/lamudi/'+prefix+file_name)    
            
        list_property_info_w = response.xpath('//div[@class="item whatsapp"]').getall()
        list_property_info = response.xpath('//div[@class="item "]').getall()
        list_all_property_info = list_property_info_w + list_property_info

        list_property_url_w = response.xpath('//div[@class="item whatsapp"]/a/@href').getall()
        list_property_url = response.xpath('//div[@class="item "]/a/@href').getall()
        list_all_property_url = list_property_url_w + list_property_url
        base_url = "https://www.lamudi.com.mx"
        list_all_property_url = [base_url + elem for elem in list_all_property_url]

        for element in zip(list_all_property_info, list_all_property_url):
            #write the files
            store_in_s3(element[1], element[0])
        
        print('\n\n+++++++++++++++++++++++++++++++++++\nFinishing one page :)\n\n+++++++++++++++++++++++++++++++++++\n')
    