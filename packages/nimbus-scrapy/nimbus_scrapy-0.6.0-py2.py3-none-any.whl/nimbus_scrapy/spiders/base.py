# -*- coding: utf-8 -*-
"""
Package Description

Configuration
=================================================================================
{
    "id": "user spider's id",
    "name": "user spider's name",
    "sid": "spider's id",
    "sname": "spider's name",
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
    "proxy": [
        "http://123.234.234.2:8000",
    ],
    "spider": {
        "date": {
            "period": "days",
            "every": 5,
        },
        "keywords": ["KEY1", "KEY2", ]
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
import hashlib
import uuid
import traceback
import scrapy
from scrapy import signals
from scrapy.spiders import Spider, CrawlSpider, CSVFeedSpider, SitemapSpider, XMLFeedSpider
from scrapy.spiders import Rule
from scrapy.http.request.form import FormRequest, Request
from scrapy.http.response.html import HtmlResponse
from scrapy.selector import Selector
from scrapy.utils.response import get_base_url
from .mixin import BaseMixin
from . import utils


class AbstractSpider(BaseMixin, Spider):
    name = None
    allowed_domains = []
    start_urls = []

    def start_requests(self):
        return super(AbstractSpider, self).start_requests()

    def parse(self, response):
        raise NotImplementedError

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        config = kwargs.pop("config", None)
        spider = super(AbstractSpider, cls).from_crawler(crawler, *args, **kwargs)
        try:
            spider.log(message=u"NAME: {}".format(spider.name), level=logging.INFO)
            if config is None:
                spider.log(message="config is None", level=logging.ERROR)
            else:
                spider.log(message=config, level=logging.DEBUG)
                spider.setup(config)
                spider.log(u"CONFIG sid:[{sid}] sname:[{sname}] version: [{version}]".format(sid=spider.sid, sname=spider.sname, version=spider.version), level=logging.INFO)
                spider.log(u"CONFIG spider_id:[{spider_id}] spider_name:[{spider_name}]".format(spider_id=spider.spider_id, spider_name=spider.spider_name), level=logging.INFO)
                spider.log(u"CONFIG config: {config}".format(spider_id=spider.spider_id, config=spider.config), level=logging.INFO)
                spider.log(u"SPIDER spider_config: {config}".format(spider_id=spider.spider_id, config=spider.spider_config), level=logging.INFO)
        except ValueError as e:
            spider.log(e, level=logging.ERROR)
            raise e
        except Exception as e:
            spider.log(e, level=logging.ERROR)
            traceback.print_exc()
        return spider

    def get_md5(self, data=None):
        m = hashlib.md5()
        m.update(data)
        return m.hexdigest()

    def get_crawled(self):
        redis = self.get_redis()
        if self.spider_id and redis:
            keys = redis.keys(u'{spider_id}*'.format(spider_id=self.spider_id))
        else:
            keys = []
        return keys

    def get_url_id(self, url=None):
        if self.spider_id and url:
            return u"{}_{}".format(self.spider_id, self.get_md5(url))
        return None

    def is_crawled(self, url=None):
        url_id = self.get_url_id(url=url)
        redis = self.get_redis()
        if redis and url_id:
            return redis.exists(url_id)
        return False

    def set_crawled(self, url=None):
        url_id = self.get_url_id(url=url)
        redis = self.get_redis()
        if redis and url_id:
            return redis.set(url_id, url)
        return False

    def generate_uid(self):
        return uuid.uuid4().hex

    def trim_value(self, value, index=0):
        if isinstance(value, basestring):
            return value
        elif isinstance(value, (tuple, list)) and len(value) > index:
            return value[index]
        elif isinstance(value, (int, long, float)):
            return value

    def datetime_to_utc(self, dt=None):
        pass

    def datetime_to_local(self, dt=None):
        pass

