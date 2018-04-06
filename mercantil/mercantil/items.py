# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MercantilItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    nombre_empresa = scrapy.Field()
    rut = scrapy.Field()
    razon_social = scrapy.Field()
    calle = scrapy.Field()
    comuna = scrapy.Field()
    ciudad = scrapy.Field()
    fono = scrapy.Field()
    importaciones = scrapy.Field()
    exportaciones = scrapy.Field()
    sitio_web = scrapy.Field()

class Categoria(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id_cat = scrapy.Field()
    nombre_categoria = scrapy.Field()

