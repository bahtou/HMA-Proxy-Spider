from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, FormRequest
from scrapy import log

from HMA_Proxy_Spider.items import rePackageItems
from HMA_Proxy_Spider.loaders import (IPPortLoader, TemporalLoader, IPDescriptLoader)

from urlparse import urljoin
from time import time


class HMA_Proxy_Spider(BaseSpider):
    '''Form Options         VARIABLE   VALUES
        # anonymity:            a[]     [0, 1, 2, 3, 4]
        # all countries:        ac[]    on/off
        # country:              c[]     'name a country' i.e. ['China', 'Brazil']
        # connection time:      ct[]    [1, 2, 3]
        # port:                 p       [3128]
        # planet lab:           pl      on/off
        # protocal:             pr[]    [0, 1, 2]
        # speed:                sp[]    [1, 2, 3]
        # Sort by:              s       [0, 1, 2, 3]
        # ASC/DESC              o       [0, 1]
        # perPage               pp      [0, 1, 2, 3]
    '''
    name = "HMA"
    allowed_domains = ["hidemyass.com"]

    def start_requests(self):
        fields = ('pr[]', 'a[]', 'sp[]', 'ct[]', 'pp')
        values = (['1', '2', '3'], ['2', '3', '4'], ['2', '3'], ['2', '3'], '3')
        return [FormRequest("http://hidemyass.com/proxy-list/", formdata=dict(zip(fields, values)), callback=self.reSendForm)]

    def reSendForm(self, response):
        return FormRequest.from_response(response, callback=self.spiderMgr)

    # The spider manager manages the responses and parsing
    def spiderMgr(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response)

        # Front page to parse
        yield self.pageParser(response)

        pages = HtmlXPathSelector(response).select("//div[@class='pagination']/li/a/@href").extract()
        for i in pages[:-1]:
            yield Request(urljoin(response.url, i), callback=self.pageParser)

    def pageParser(self, response):
        # log.msg("URL to parse: %s" % response.url, level=log.INFO)

        ipPLoader = IPPortLoader(response=response)
        tempLoader = TemporalLoader(response=response)
        ipDescripLoader = IPDescriptLoader(response=response)

        tempLoader.add_value('loadTime', time())
        ipPLoader.add_xpath('Port', "//table[@id='listtable']/tr/td[3]/text()")
        tempLoader.add_xpath('lastUpdate', "//table[@id='listtable']/tr/td[1]/@rel")
        ipDescripLoader.add_xpath('Country', "//*[@class='country']/text()")
        ipDescripLoader.add_xpath('speedValue', "//*[@class='speedbar response_time']/@rel")
        ipDescripLoader.add_xpath('speedDesc', "//*[@class='speedbar response_time']/div/@class")
        ipDescripLoader.add_xpath('connTimeValue', "//*[@class='speedbar connection_time']/@rel")
        ipDescripLoader.add_xpath('connTimeDesc', "//*[@class='speedbar connection_time']/div/@class")
        ipDescripLoader.add_xpath('proxyType', "//table[@id='listtable']/tr/td[7]/text()")
        ipDescripLoader.add_xpath('Anonymity', "//table[@id='listtable']/tr/td[8]/text()")

        # IP address XPaths
        span = HtmlXPathSelector(response).select("//table[@id='listtable']/tr/td[2]/span")
        Xpaths = self.extractXPaths(span)
        ipPLoader.add_value('IP_Address', Xpaths)

        items = [ipPLoader.load_item(), tempLoader.load_item(), ipDescripLoader.load_item()]
        # log.msg("Items: %s" % items, level=log.INFO)
        return self.rePackIt(items)

    # Xpaths to be passed to the processor
    def extractXPaths(self, span):
        nodeList = []
        disNone = []
        for i in span:
            nodeList.append(i.select("node()").extract())
            disNone.append(i.select('span[@style="display:none"] | div[@style="display:none"]').extract())
        return nodeList, disNone

    # Repackage items from loaders into a single package
    def rePackIt(self, items):
            rePackage = rePackageItems()
            for item in items:
                for key, value in item.items():
                    rePackage.fields[key] = value
            return rePackage
