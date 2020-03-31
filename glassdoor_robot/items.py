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
  search_name = scrapy.Field()
  glassdoor_company_name = scrapy.Field()
  summary = scrapy.Field()
  author_title = scrapy.Field()
  author_location = scrapy.Field()
  recommends_flag = scrapy.Field()
  outlook_flag = scrapy.Field()
  ceo_opinion_flag = scrapy.Field()
  main_text_description = scrapy.Field()
  pros_description = scrapy.Field()
  cons_description = scrapy.Field()
  advice_to_management_description = scrapy.Field()
  star_rating_overall = scrapy.Field()
  star_rating_work_life_balance = scrapy.Field()
  star_rating_culture_and_values = scrapy.Field()
  star_rating_career_opportunities = scrapy.Field()
  star_rating_comp_and_benefits = scrapy.Field()
  star_rating_senior_management = scrapy.Field()
  review_date = scrapy.Field()
