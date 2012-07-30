from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy import log

from twisted.enterprise import adbapi


class HmaProxySpiderPipeline(object):
    '''
        Application of twisted adbapi.
        Passing scrapy container items into a MySQL database.
        Assume the db is already created.
    '''
    def __init__(self):
        log.msg('Pipes Ready!', level=log.INFO)
        dispatcher.connect(self.spider_opened, signals.spider_opened)

    def spider_opened(self, spider):
        log.msg('Connceting to MySQL', level=log.INFO)
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            db="db_name",
                                            user='user_name',
                                            passwd='pass_word'
                                            )

    def process_item(self, item, spider):
        input = self.dbpool.runInteraction(self._ips_insert, item)
        input.addErrback(self.handle_error)

    def _ips_insert(self, tx, item):
        items = item.fields
        sql = "INSERT INTO Proxies(IP_Address, Port, loadTime, lastUpdate, Country, speedValue, speedDesc, connTimeValue, connTimeDesc, proxyType, Anonymity) \
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        for i in range(len(items['IP_Address'])):
            tx.execute(sql, \
                (items['IP_Address'][i], items['Port'][i], items['loadTime'][0], items['lastUpdate'][i], items['Country'][i], items['speedValue'][i], items['speedDesc'][i], \
                items['connTimeValue'][i], items['connTimeDesc'][i], items['proxyType'][i], items['Anonymity'][i]))

    def handle_error(self, e):
        log.err("Error: %s" % e)
