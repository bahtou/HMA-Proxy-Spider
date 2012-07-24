BOT_NAME = 'HMA_Proxy_Spider'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['HMA_Proxy_Spider.spiders']
NEWSPIDER_MODULE = 'HMA_Proxy_Spider.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)


DOWNLOAD_DELAY = 2

PATH_DEBUG = True
PATH_DEBUG_URL_LENGTH = 97

ITEM_PIPELINES = ['HMA_Proxy_Spider.pipelines.HmaProxySpiderPipeline']

# Maximum number of concurrent items (per response) to process in parallel in the Item Processor (also known as the Item Pipeline).
CONCURRENT_ITEMS = 100

# The maximum number of concurrent (ie. simultaneous) requests that will be performed by the Scrapy downloader.
# The maximum number of requests that the request_container can fill-up.  The container is filled to capacity with the requests.  Then as one exits, another fills its spot.  When there are no more requests to fill a vacancy, the container simply empties.
# This effect is most noticibly when 'Closing spider (shutdown)'
CONCURRENT_REQUESTS = 8

# The maximum number of concurrent (ie. simultaneous) requests that will be performed to any single domain.
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# The maximum number of concurrent (ie. simultaneous) requests that will be performed to any single IP. If non-zero, the CONCURRENT_REQUESTS_PER_DOMAIN setting is ignored, and this one is used instead. In other words, concurrency limits will be applied per IP, not per domain
CONCURRENT_REQUESTS_PER_IP = 0

DOWNLOADER_STATS = True
RANDOMIZE_DOWNLOAD_DELAY = True
