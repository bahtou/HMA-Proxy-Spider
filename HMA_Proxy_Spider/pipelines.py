from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy import log

import MySQLdb


class HmaProxySpiderPipeline(object):
    '''
        Passing scrapy container items into a MySQL database.
        Assume the db is already created.
    '''
    def __init__(self):
        log.msg('Pipes Ready!', level=log.INFO)
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self, spider):
        log.msg('Connceting to MySQL', level=log.INFO)
        try:
            self.conn = MySQLdb.connect(
                        host="host_name",
                        user="user_name",
                        passwd="password",
                        db="db_name")
            self.cursor = self.conn.cursor()
        except MySQLdb.Error, e:
            log.msg("Error %d: %s" % (e.args[0], e.args[1]), level=log.DEBUG)

    def spider_closed(self, spider):
        self.cursor.close()
        self.conn.close()
        log.msg('Disconnceted from MySQL', level=log.INFO)

    def process_item(self, item, spider):
        items = item.fields
        sql = "INSERT INTO Proxies(IP_Address, Port, loadTime, lastUpdate, Country, speedValue, speedDesc, connTimeValue, connTimeDesc, proxyType, Anonymity) \
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            for i in range(len(items['IP_Address'])):
                self.cursor.execute(sql, \
                    (items['IP_Address'][i], items['Port'][i], items['loadTime'][0], items['lastUpdate'][i], items['Country'][i], items['speedValue'][i], items['speedDesc'][i], \
                    items['connTimeValue'][i], items['connTimeDesc'][i], items['proxyType'][i], items['Anonymity'][i]))
            self.conn.commit()
        except MySQLdb.Error, e:
            log.msg("Error %d: %s" % (e.args[0], e.args[1]), level=log.DEBUG)
