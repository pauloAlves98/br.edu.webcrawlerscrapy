# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import requests
from os import path, makedirs
import re

#tem como usar as próprias configurações do scrapy pra baixar (scrapy.pipelines.images.ImagesPipeline)
class MegafilmesPipeline(object):
    # def __init__(self):
    #     self.image_dir = path.dirname(path.abspath(__file__)) + "/../images"
    #     if not path.exists(self.image_dir):
    #         makedirs(self.image_dir)

    def process_item(self, item, spider):
        image_dir = path.dirname(path.abspath(__file__)) + "/../images/"+item["nomeArquivo"]
        if not path.exists(image_dir):
            makedirs(image_dir)

        try:
            image_url = item["image_urls"]
            filename = item["titulo"]
            #Renomeia a Imagem e Extensão
            filepath = image_dir + "/" + filename+"."+re.search(r"\.(\w+)$", str(image_url[0])).group(1)
            item["images"] = filename
            r = requests.get(str(image_url[0]))#requisição para baixar o content
            with open(filepath, 'wb') as outfile:
                outfile.write(r.content)
            return item
        except Exception as e:
            print("Exception--------------")
            print(e)
            return item

