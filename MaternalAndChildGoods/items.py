# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import time
#time.strftime('%Y-%m-%d %H:%M:%S')
# Scraped texts from website
class Text(scrapy.Item):
    # cls_tag = 0
    cls_tag = scrapy.Field()
    time = scrapy.Field()
    text = scrapy.Field()
    topic = scrapy.Field()
    follower_cnt = scrapy.Field()
    top_cnt = scrapy.Field()

#Scraped images from website
class ImageUrl(scrapy.Item):
    # cls_tag = 1
    cls_tag = scrapy.Field()
    time = scrapy.Field()
    src = scrapy.Field()
    title = scrapy.Field()

class Topic(scrapy.Item):
    # cls_tag = 2  
    cls_tag = scrapy.Field()
    href = scrapy.Field()
    ttext = scrapy.Field()
    view_cnt = scrapy.Field()
    reply_cnt = scrapy.Field()
    time = scrapy.Field()
    # we reserve tag field because for some websites, 
    # topics are naturally classified when they are posted
    # NOT IMPLEMENTED
    tag = scrapy.Field()
    pass 