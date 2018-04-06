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
from mercantil.items import MercantilItem

class MercantilSpider(Spider):

	name = 'mercantil36_cat'
	allowed_domains = ['mercantil.com']

	custom_settings = {'TOR_RENEW_IDENTITY_ENABLED': True, 'TOR_ITEMS_TO_SCRAPE_PER_IDENTITY': 40}

	download_delay = 2

	def start_requests(self): 
			
		cat = getattr(self, 'cat', None)
		if cat is not None:
			url_inicio = 'https://www.mercantil.com/rc/mas_empresas.asp?lang=esp&code=' + cat + '&lastmsg=0'
		yield Request(url=url_inicio, callback=self.parse, dont_filter=True)

	def parse(self, response):

		sel1 = Selector(response)
		empresas = sel1.xpath('//h2/a[@id="compLink"]')
		next_page =  response.xpath('//div[contains(@id, "viewmore")]').extract_first()

		if not empresas:

			raise CloseSpider('Listeilor...')

		else:
		
			for num, href in enumerate(response.xpath('//h2/a[@id="compLink"]/@href').extract()):

				url_empresa = 'https://www.mercantil.com' + href

				yield Request(url_empresa, callback=self.parse_empresa)

			next_page =  response.xpath('//div[contains(@id, "viewmore")]').extract_first()

			if next_page is not None:

				params = parse_qs(urlparse(response.url)[4])
				params = dict( (k, v if len(v)>1 else v[0] )
					for k, v in params.items() )
				
				params['lastmsg'] = int(params['lastmsg'])
				params['code'] = int(params['code'])
				params['lastmsg'] += 1
				current_msg = open('lastmsg', 'w')
				current_msg.write(str(params['lastmsg']))
				current_msg.close()
				url_sgte = "https://www.mercantil.com/rc/mas_empresas.asp?" + urlencode(params)
			
				yield Request(url=url_sgte, callback=self.parse)

			else:

				raise CloseSpider('Listeilor...')

	def parse_empresa(self, response):
	
		sel2 = Selector(response)
		empresas2 = sel2.xpath('//h1/a[@id="compLink"]/text()')

		if not empresas2:
			
			print('No hay datos de empresa.')

		item = MercantilItem()
		item['nombre_empresa'] = response.xpath('//h1/a[@id="compLink"]/text()').extract_first()
		item['rut'] = response.xpath('//div[@id="caja_detalle"]/div[1]/div[2]/span/text()').extract_first() # hardcodeado, ojo
		item['razon_social'] = response.xpath('//div[@id="caja_detalle"]/div[@class="primer_detalle"]//span[@itemprop="name"]/text()').extract_first()
		item['calle'] = response.xpath('//a[@id="_address2"]/span[@itemprop="streetAddress"]/text()').extract_first()
		item['comuna'] = response.xpath('//a[@id="_address2"]/span[@itemprop="addressLocality"]/text()').extract_first()
		item['ciudad'] = response.xpath('//a[@id="_address2"]/span[@itemprop="addressRegion"]/text()').extract_first()
		item['fono'] = response.xpath('//span[@id="_telephone7"]/a/text()').extract_first()
		item['importaciones'] = response.xpath('//div[@id="caja_detalle"]//a[contains(@href,"ie=1")]/text()').extract_first()
		item['exportaciones'] = response.xpath('//div[@id="caja_detalle"]//a[contains(@href,"ie=2")]/text()').extract_first()
		item['sitio_web'] = response.xpath('//span[@id="_url3"]//a/strong/text()').extract_first()

		yield item


