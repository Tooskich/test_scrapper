# -*- coding: utf-8 -*-
from scrapy.selector import Selector

from scrapy.spider import BaseSpider
from scrapy.http import Request

from tooski.items import TooskiRanking


class RankingSpider(BaseSpider):
    # nom du crawler à spécifier lors de l'exécution
    name = 'ranking'

    # domaine(s) sur le ou lesquels le crawler aura le droit d'aller
    allowed_domains = ['www.fis-ski.com']

    def start_requests(self):
        yield Request('http://www.fis-ski.com/alpine-skiing/leader-board/',
                      callback=self.parse_item)

    def parse_item(self, response):
        hxs = Selector(response)
        item = TooskiRanking()
        item['link'] = response.url

        rows = hxs.xpath('//div[contains(@class, "dcm-leaderBoard")]//tr')
        men = []
        women = []
        men_flag = 0
        for row in rows:
            name = row.xpath(
                'td/div/a/span[contains(@class, "dcm-athName")]/text()').extract()
            country = row.xpath(
                'td/div/div[contains(@class, "dcm-noc")]/text()').extract()
            row = row.xpath('td/text()').extract()
            if row and int(row[0]) <= 25:
                place = row[0]
                score = row[2]
                name = name[0]
                country = country[0]
                if int(row[0]) == 1:
                    men_flag += 1
                if men_flag >= 2:
                    men.append([place, name, country, score])
                else:
                    women.append([place, name, country, score])

        item['men'] = men
        item['women'] = women
        return item
