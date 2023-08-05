# -*- coding: utf-8 -*-
from __future__ import absolute_import
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
        pipelines = crawler.settings["ITEM_PIPELINES"]
        if not isinstance(pipelines, dict):
            crawler.settings["ITEM_PIPELINES"] = {
                "nimbus_scrapy.pipelines.NimbusPipeline": 200,
            }
        elif isinstance(pipelines, dict):
            crawler.settings["ITEM_PIPELINES"]["nimbus_scrapy.pipelines.NimbusPipeline"] = 200
        spider = super(AbstractSpider, cls).from_crawler(crawler, *args, **kwargs)
        try:
            if config is None:
                spider.log(message="config is None", level=logging.WARNING)
            else:
                spider.setup(config)
        except Exception as e:
            spider.log(e)
        return spider



