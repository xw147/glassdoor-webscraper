# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# Configuration
import pymongo
import json

from glassdoor_robot.items import GlassdoorCompanyItem, GlassdoorReviewItem

mongo_conf = None
with open("config.json") as config_file:
  mongo_conf = json.load(config_file)['MongoDbConfig']


class GlassdoorRobotPipeline(object):

  def __init__(self):
    connection = pymongo.MongoClient(
      mongo_conf['Server'],
      mongo_conf['Port']
    ) 
    db = connection[mongo_conf['Database']]
    self.company_collection = db[mongo_conf['CompanyCollection']]
    self.review_collection = db[mongo_conf['ReviewCollection']]

  
  def process_review_item(self, item, spider):
    self.review_collection.insert(dict(item))
    return item

  def process_company_item(self, item, spider):
    self.company_collection.insert(dict(item))
    return item

  def process_item(self,item,spider):
    
    if isinstance(item, GlassdoorReviewItem):	
      self.review_collection.insert(dict(item))	
    elif isinstance(item, GlassdoorCompanyItem):
      self.company_collection.insert(dict(item))
    return item
