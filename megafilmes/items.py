# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader

class MegafilmesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
   # image_urls = scrapy.Field()
   # images = scrapy.Field()
    titulo = scrapy.Field()
    ano = scrapy.Field()
    elenco = scrapy.Field()
    duracao = scrapy.Field()
    tipo = scrapy.Field()
    link = scrapy.Field()
    nomeArquivo = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

  #  nomeFile = scrapy.Field()




