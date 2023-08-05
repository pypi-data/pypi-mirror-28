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
    sid = None
    sname = None
    spider_id = None
    spider_name = None
    spider_config = {}

    _db = None
    _redis = None
    _proxy = None

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
        self.sid = self.config.pop("sid", None)
        self.sname = self.config.pop("sname", None)
        self.spider_id = self.config.pop("id", None) or self.config.pop("spider_id", "default")
        self.spider_name = self.config.pop("name", None) or self.config.pop("spider_name", self.name)
        for key, value in self.config.iteritems():
            func = getattr(self, u"_setup_{}".format(key), None) or getattr(self, u"setup_{}".format(key), None)
            if func and callable(func):
                v = func(self.spider_id, value)
                setattr(self, u"_{}".format(key), v)
            elif value:
                setattr(self, key, value)

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

    def _setup_proxy(self, spider_id=None, config=None):
        if config is None:
            raise ValueError(u"ERROR proxy:{}".format(config))
        return copy.deepcopy(config)

    def get_db(self):
        return self._db

    def get_redis(self):
        return self._redis

    def get_proxy(self):
        return self._proxy

    def process_item(self, item, spider, **kwargs):
        raise NotImplementedError


