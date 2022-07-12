# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GlassdoorRobotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GlassdoorCompanyItem(scrapy.Item):
  search_name = scrapy.Field()
  glassdoor_company_name = scrapy.Field()
  industry = scrapy.Field()
  headquarters = scrapy.Field()
  company_type = scrapy.Field()
  size = scrapy.Field()

class GlassdoorReviewItem(scrapy.Item):
    
  review_date = scrapy.Field()
  employee_title = scrapy.Field()
  employee_location = scrapy.Field()
  employee_status = scrapy.Field()
  
  review_title = scrapy.Field()
  helpful_count = scrapy.Field()
  pros = scrapy.Field()
  cons = scrapy.Field()

  
  rating_overall = scrapy.Field()
  rating_balance = scrapy.Field()
  rating_culture = scrapy.Field()
  rating_diversity = scrapy.Field()
  rating_career = scrapy.Field()
  rating_comp = scrapy.Field()
  rating_mgmt = scrapy.Field()
  
  recommends = scrapy.Field()
  positive_outlook = scrapy.Field()
  approves_of_CEO = scrapy.Field()
 
  
  # main_text_description = scrapy.Field()
  # search_name = scrapy.Field()
  # glassdoor_company_name = scrapy.Field()
  # advice_to_management_description = scrapy.Field()
  
  
