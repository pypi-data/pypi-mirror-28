# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import sys
import json
import datetime
import time
import urlparse
import random
import platform
import copy
import scrapy
from scrapy import signals
from scrapy.spiders import Spider, CrawlSpider, CSVFeedSpider, SitemapSpider, XMLFeedSpider
from scrapy.spiders import Rule, BaseSpider
from scrapy.exceptions import DropItem
from scrapy.exceptions import NotConfigured, IgnoreRequest
from scrapy.http.request.form import FormRequest, Request
from scrapy.http.response.html import HtmlResponse
from scrapy.selector import Selector
from scrapy.utils.response import get_base_url

__all__ = ["BaseMixin", ]


class BaseMixin(object):
    config = None
    spider_id = None
    spider_config = None

    def setup(self, config=None):
        if config is None:
            self.config = None
        elif isinstance(config, basestring):
            self.config = json.loads(config)
        elif isinstance(config, dict):
            self.config = copy.deepcopy(config)
        else:
            raise NotImplementedError
        if self.config is None:
            return
        self.spider_id = self.config.get("id", "spider_id")
        for key, value in self.config.iteritems():
            func_key = u"setup_{}".format(key)
            func = getattr(self, func_key, None)
            if callable(func):
                client = func(self.spider_id, value)
            else:
                client = None
            setattr(self, key, client)

    def setup_db(self, spider_id=None, config=None):
        from ..data import dbclient
        dbclient.init(name=spider_id, **config)
        return dbclient.get_session(name=spider_id)

    def setup_redis(self, spider_id=None, config=None):
        from ..data import redisclient
        connection = redisclient.init(name=spider_id, **config)
        return connection

    def setup_spider(self, spider_id=None, config=None):
        self.spider_config = copy.deepcopy(config)
        return self.spider_config

    def process_item(self, item, spider, **kwargs):
        raise NotImplementedError


