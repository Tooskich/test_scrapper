# -*- coding: utf-8 -*-
from scrapy.selector import Selector

from scrapy.spider import BaseSpider
from scrapy.http import Request

from tooski.items import TooskiNews


class MyCrawlerSpider(BaseSpider):
    # nom du crawler à spécifier lors de l'exécution
    name = 'tooski'

    # domaine(s) sur le ou lesquels le crawler aura le droit d'aller
    allowed_domains = ['data.fis-ski.com']
    max_newsid = 15

    def start_requests(self):
        for i in xrange(self.max_newsid):
            yield Request(
                'http://data.fis-ski.com/dynamic/results.html?sector=AL&raceid=%d' % i,
                callback=self.parse_item)

    def parse_item(self, response):
        hxs = Selector(response)
        item = TooskiNews()
        url = response.url
        item['id'] = url[url.index('raceid=') + 7:]
        item['location'] = hxs.xpath(
            '//div[contains(@class, "padding-content")]/h3/a/text()').extract()[0].strip()
        item['type'] = hxs.xpath(
            '//div[contains(@class, "padding-content")]/div/div/h4/text()').extract()[0].strip()
        item['link'] = url
        item['date'] = hxs.xpath(
            '//div[contains(@class, "padding-content")]/h3/span/text()').extract()[0].strip()

        return item
