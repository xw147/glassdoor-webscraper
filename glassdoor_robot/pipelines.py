# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# Configuration

# import pymongo
# import json
#
# from glassdoor_robot.items import GlassdoorCompanyItem, GlassdoorReviewItem
#
# mongo_conf = None
# with open("config.json") as config_file:
#   mongo_conf = json.load(config_file)['MongoDbConfig']
#
#
# class GlassdoorRobotPipeline(object):
#
#   def __init__(self):
#     connection = pymongo.MongoClient(
#       mongo_conf['Server'],
#       mongo_conf['Port']
#     ) 
#     db = connection[mongo_conf['Database']]
#     self.company_collection = db[mongo_conf['CompanyCollection']]
#     self.review_collection = db[mongo_conf['ReviewCollection']]
#
#
#   def process_review_item(self, item, spider):
#     self.review_collection.insert(dict(item))
#     return item
#
#   def process_company_item(self, item, spider):
#     self.company_collection.insert(dict(item))
#     return item
#
#   def process_item(self,item,spider):
#
#     if isinstance(item, GlassdoorReviewItem):	
#       self.review_collection.insert(dict(item))	
#     elif isinstance(item, GlassdoorCompanyItem):
#       self.company_collection.insert(dict(item))
#     return item

from scrapy import signals
from scrapy.exporters import CsvItemExporter

class CsvExportPipeline(object):

    def __init__(self):
      self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
      pipeline = cls()
      crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
      crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
      return pipeline

    def spider_opened(self, spider):
        file = open('/Users/work/glassdoor-webscraper/glassdoor_robot/test.csv', 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.fields_to_export = ['review_date','employee_title','employee_location','employee_status',
                                          'review_title','helpful_count','pros','cons',
                                          'rating_overall', 'rating_balance', 'rating_culture',
                                          'rating_diversity', 'rating_career', 'rating_comp', 'rating_mgmt',
                                          'recommends', 'positive_outlook', 'approves_of_CEO']
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

