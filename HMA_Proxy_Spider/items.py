from scrapy.item import Item, Field
from scrapy import log


class IP_Port(Item):
    log.msg("Creating Item Containers", level=log.INFO)
    IP_Address = Field()
    Port = Field()


class TemporalItems(Item):
    loadTime = Field()
    lastUpdate = Field()


class IPDescriptions(Item):
    Country = Field()
    speedValue = Field()
    speedDesc = Field()
    connTimeValue = Field()
    connTimeDesc = Field()
    proxyType = Field()
    Anonymity = Field()


class rePackageItems(Item):
    '''Repackage items'''
    pass
