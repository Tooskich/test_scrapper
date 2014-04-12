# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy.spider import BaseSpider
from scrapy.http import Request

from tooski.items import TooskiNews


class MyCrawlerSpider(BaseSpider):
    # nom du crawler à spécifier lors de l'exécution
    name = 'tooski'

    # domaine(s) sur le ou lesquels le crawler aura le droit d'aller
    allowed_domains = ['data.fis-ski.com']
    max_newsid = 150

    # point de départ : vous pouvez mettre une liste d'url, séparées par des
    # virgules
    # start_urls = ['http://www.tooski.ch']

    # très important : les régles en fonction du schéma des urls (c'est des
    # regexp)
    # rules = [
    # on autorise /article et que l'on va parser avec la methode
    # parse_item, et que l'on va aussi suivre pour extraire des liens
    #     Rule(SgmlLinkExtractor(allow=['\/comment.php']),
    #          callback='parse_item', follow='True'),

    # on autorise le crawler à parcourir et à extraire des liens de tous
    # les .html, mais pas si y'a /about dans l'url
    #     Rule(SgmlLinkExtractor(allow=['\*.php*', '\.php?id=\d+', '\.php?p=\d+'],
    #          deny=['\/about']), follow='True')
    # ]
    def start_requests(self):
        for i in xrange(self.max_newsid):
            yield Request(
                'http://data.fis-ski.com/dynamic/results.html?sector=AL&raceid=%d' % i,
                callback=self.parse_item)

    def parse_item(self, response):
        hxs = Selector(response)
        item = TooskiNews()
        item['title'] = hxs.xpath(
            '//div[contains(@class, "padding-content")]/h3/a/text()').extract()[0]
        item['link'] = response.url

        # exemples de scrap plus complexes avec des regexp :
        # item['datereview'] = mtabletd.select('./tr[position()=2]/td[position()=3]/strong/text()').re(r'em (.*)$')
        # item['note'] = mtabletd.select('./tr[position()=2]/td/table/tr/td[position()=3]/img/@src').re(r'avloja_m([0-9]+).gif')
        # item['textreview'] = mtabletd.select('./tr[position()=4]/td/div/p/span[@class="opncomp"]/text()').extract()

        return item
