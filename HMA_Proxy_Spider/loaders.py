from scrapy.contrib.loader.processor import MapCompose, Identity
from scrapy.contrib.loader import XPathItemLoader
from scrapy import log

from HMA_Proxy_Spider.items import (IP_Port, TemporalItems, IPDescriptions)
from HMA_Proxy_Spider.processors import GetIPAddresses


class RootItemLoader(XPathItemLoader):
    default_input_processor = Identity()
    default_ouput_processor = Identity()


class IPPortLoader(RootItemLoader):
    log.msg("PortLoading", level=log.INFO)
    default_item_class = IP_Port
    Port_in = MapCompose(unicode.strip, int)
    IP_Address_in = GetIPAddresses()


class TemporalLoader(RootItemLoader):
    default_item_class = TemporalItems
    lastUpdate_in = MapCompose(int)


class IPDescriptLoader(RootItemLoader):
    default_item_class = IPDescriptions
    speedValue_in = MapCompose(int)
    connTimeValue = MapCompose(int)
