# -*- coding: utf-8 -*-
from __future__ import absolute_import
import scrapy


class CrawledItem(scrapy.Item):
    url = scrapy.Field()


class ScrapItem(scrapy.Item):
    url = scrapy.Field()


