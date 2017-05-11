# -*- coding: utf-8 -*-
import scrapy
import re

class StocksSpider(scrapy.Spider):
    name = "stocks"
    #allowed_domains = ["gupiao.baidu.com"]
    download_delay = 1
    start_urls = ['http://quote.eastmoney.com/stocklist.html']

    def parse(self, response):
        for href in response.css('a::attr(href)').extract():
            try:
                stock = re.findall(r"[s][hz][603]\d{5}",href)[0]
                url = 'https://gupiao.baidu.com/stock/'+stock+'.html'
                yield scrapy.Request(url,callback=self.parse_res)
            except:
                continue

    def parse_res(self,response):
        infoDict = {}
        item = response.css('.stock-bets')
        name = item.css('.bets-name').extract()[0]
        keyList = item.css('dt').extract()
        valueList = item.css('dd').extract()
        for i in range(len(keyList)):
            key = re.findall(r'>.*</dt>',keyList[i])[0][1:-5]
            try:
                val = re.findall(r'\d+\.?.*</dd>',valueList[i])[0][0:-5]
            except:
                val = '--'
            infoDict[key] = val

        infoDict.update({'股票名称':re.findall('\s.*\(',name)[0].split()[0]+re.findall('\>.*\<',name)[0][1:-1]})
        yield infoDict
