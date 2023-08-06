# -*- coding: utf-8 -*-
from __future__ import absolute_import


class NimbusPipeline(object):

    def process_item(self, item, spider, **kwargs):
        func = getattr(spider, "process_item", None)
        if callable(func):
            item = func(item=item, spider=spider, **kwargs)
        return item

