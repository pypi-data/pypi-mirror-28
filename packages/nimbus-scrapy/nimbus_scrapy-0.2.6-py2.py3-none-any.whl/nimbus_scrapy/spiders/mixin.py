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
        self.spider_id = self.config.get("id", None) or self.config.get("spider_id", "default")
        for key, value in self.config.iteritems():
            prifunc_key = u"_setup_{}".format(key)
            pubfunc_key = u"setup_{}".format(key)
            func = getattr(self, prifunc_key, None) or getattr(self, pubfunc_key, None)
            if callable(func):
                client = func(self.spider_id, value)
            else:
                client = None
            setattr(self, key, client)

    def _setup_db(self, spider_id=None, config=None):
        from ..data import dbclient
        if not isinstance(config, dict):
            raise ValueError(u"ERROR db:{}".format(config))
        dbclient.init(name=spider_id, **config)
        return dbclient.get_session(name=spider_id)

    def _setup_redis(self, spider_id=None, config=None):
        from ..data import redisclient
        if not isinstance(config, dict):
            raise ValueError(u"ERROR redis:{}".format(config))
        connection = redisclient.init(name=spider_id, **config)
        return connection

    def _setup_spider(self, spider_id=None, config=None):
        if not isinstance(config, dict):
            raise ValueError(u"ERROR spider:{}".format(config))
        self.spider_config = copy.deepcopy(config)
        return self.spider_config

    def _setup_spider_config(self, spider_id=None, config=None):
        if not isinstance(config, dict):
            raise ValueError(u"ERROR spider_config:{}".format(config))
        self.spider_config = copy.deepcopy(config)
        return self.spider_config

    def process_item(self, item, spider, **kwargs):
        raise NotImplementedError


