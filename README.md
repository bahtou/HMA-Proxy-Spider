HMA-Proxy-Spider
================

Spider that crawls for IP addresses

Using Scrapy to scrape proxy information from the site hidemyass.com/proxy-list.

The data extracted is dumped into a MySQL database that is assumed to be created.
See 'mysql_table/proxies.sql' for table information
See piplelines.py for DB credentials

Scattered throughout are logs to help identify some problem areas


Execute:
scrapy crawl HMA