# -*- coding: utf-8 -*-
# scrapy crawl mercantil36 -o mercantil_part.csv -s JOBDIR=jobdir

"""
Created on Mon Feb 12 23:46:07 2018

@author: IL DEIVID
"""
from scrapy import Spider
from scrapy import Selector
from scrapy import Request
from scrapy.exceptions import CloseSpider
from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.parse import urlencode
from mercantil.items import Categoria

class MercantilSpider(Spider):

	name = 'mercantil36_categoria'
	allowed_domains = ['mercantil.com']

	custom_settings = {'TOR_RENEW_IDENTITY_ENABLED': True, 'TOR_ITEMS_TO_SCRAPE_PER_IDENTITY': 10}

	download_delay = 2


	def start_requests(self): 
		i = 1
		urls = []
		while True:
			urls.append('https://www.mercantil.com/farmacias/' + str(i) + '/')
			i += 1
			if i == 15000:
				break

		for url in urls:
			yield Request(url=url, callback=self.parse)

	def parse(self, response):
	
		cat1 = response.url.replace('https://www.mercantil.com/farmacias/','')
		cat2 = cat1.replace('/','')

		item = Categoria()
		item['id_cat'] = cat2
		item['nombre_categoria'] = response.xpath("//h1[@class='mayuscula']/a/@title").extract_first()

		yield item


