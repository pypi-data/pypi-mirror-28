# -*- coding: utf-8 -*-
"""
Package Description

Configuration
=================================================================================
{
    "db": {
        "db_uri": "{dialect}{user}:{password}@{host}:{port}/{db}",
        "dialect": "postgresql://",
        "host": "xxx.xxx.xxx.xxx",
        "port": "5432",
        "db": "xxx",
        "user": "xxx",
        "password": "xxx"
    },
    "redis": {
        "host": '127.0.0.1',
        "port": 6379,
        "db": 0,
        "password": None
    },
    "spider_config": {
        "time": "",
        "keywords": [
            ""
        ]
    }
}

"""
import os
import sys
import json
import logging
import datetime
import time
import urlparse
import random
import platform
import scrapy
from scrapy import signals
from scrapy.spiders import Spider, CrawlSpider, CSVFeedSpider, SitemapSpider, XMLFeedSpider
from scrapy.spiders import Rule
from scrapy.http.request.form import FormRequest, Request
from scrapy.http.response.html import HtmlResponse
from scrapy.selector import Selector
from scrapy.utils.response import get_base_url
from .mixin import BaseMixin


class AbstractSpider(BaseMixin, Spider):
    name = None
    allowed_domains = []
    start_urls = []

    def __init__(self, name=None, **kwargs):
        super(AbstractSpider, self).__init__(name, **kwargs)

    def start_requests(self):
        return super(AbstractSpider, self).start_requests()

    def parse(self, response):
        raise NotImplementedError

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        config = kwargs.pop("config", None)
        spider = super(AbstractSpider, cls).from_crawler(crawler, *args, **kwargs)
        try:
            if config is None:
                spider.log(message="config is None", level=logging.ERROR)
            else:
                spider.setup(config)
        except Exception as e:
            spider.log(e)
        return spider



