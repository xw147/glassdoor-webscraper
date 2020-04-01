# Python Standards
import sys
import json
from time import sleep
from urllib.parse import urlencode
import random 

# Scrapy
import scrapy
from scrapy.spiders.init import InitSpider
from glassdoor_robot.items import GlassdoorCompanyItem, GlassdoorReviewItem

# Selenium
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys

# Configuration
configuration = None
with open("config.json") as config_file:
  configuration = json.load(config_file)

class GlassdoorSpider(InitSpider):
  name = "glassdoor_spider"

  def __init__(self, company_name, **kwargs):
    self.company_name = company_name
    self.cookies = None
    self.configuration = configuration
   
  def custom_wait(self):
    min_time = 5.0
    max_time = 10.0
    sleep(random.uniform(min_time,max_time))
    return True

  def init_request(self):   
    # Login to Glassdoor using Selenium
    driver = webdriver.Firefox(executable_path="./drivers/geckodriver")
    driver.get("https://www.glassdoor.co.uk")
    # Apply wait condition to prevent overloading the server with requests
    self.custom_wait()    
    # Submit login credentials into form
    driver.find_element_by_class_name('sign-in').click()
    self.custom_wait()
    driver.find_element_by_name('username').send_keys(
      configuration["GlassdoorConfig"]["Username"])
    self.custom_wait() 
    driver.find_element_by_name('password').send_keys(
      configuration["GlassdoorConfig"]["Password"], Keys.ENTER)
    # Store the authenticated cookies so they can be copied to scrapy
    self.cookies = driver.get_cookies()
    # Close the web browser
    driver.quit()
    self.custom_wait()    
    # Generate request for the company search
    form_data = {'sc.keyword': self.company_name}
    yield scrapy.Request(
      "https://www.glassdoor.co.uk/Reviews/company-reviews.htm?" + 
      urlencode(form_data), 
      cookies=self.cookies, 
      callback=self.auth_company_search_parse
    )

  def auth_company_search_parse(self, response):
    # If the search returned multiple results the url contains SRCH
    if 'SRCH' in response.url:
      company_page_link = response.css('a.tightAll.h2::attr(href)'
        ).extract_first()
      self.custom_wait()
      yield scrapy.Request('https://www.glassdoor.co.uk'+company_page_link, 
        cookies = self.cookies,
        callback=self.company_info_parse)
    # Else the request leads to the company page directly
    else:
      for item in self.company_info_parse(response):
        
        yield item
    # Simultaneously navigate to the reviews page for extraction
    follow_link = response.css('a.reviews::attr(href)').extract_first()
    self.custom_wait()
    yield scrapy.Request('https://www.glassdoor.co.uk'+follow_link, 
      cookies=self.cookies,
      callback=self.company_reviews_parse)
   

  def company_info_parse(self, response):
    # This code triggers when the company overview page has been loaded
    # Build the object to be processed and stored
    company_item = GlassdoorCompanyItem()
    company_item['search_name'] = self.company_name
    company_item['glassdoor_company_name']=response.css('div.header.cell.info'+ 
      ' h1.strong.tightAll::attr(data-company)').extract_first() 
    company_info = response.css('div.infoEntity')
    info_dict = {}
    for info_item in company_info:
      key = info_item.css('label::text').extract_first()
      value = info_item.css('span.value::text').extract_first()
      info_dict[key]=value

    company_item['industry'] = (info_dict['Industry']  
      if 'Industry' in info_dict else None)
    company_item['headquarters'] = (info_dict['Headquarters'] 
      if 'Headquarters' in info_dict else None)
    company_item['company_type'] = (info_dict['Type'] 
      if 'Type' in info_dict else None)
    company_item['size'] = (info_dict['Size'] 
      if 'Size' in info_dict else None)
    yield company_item

  
  def company_reviews_parse(self, response):
    #Iterate through each review element in the DOM tree
    reviews = response.css('ol.empReviews li.empReview')
    #Identify the opinions section and select the three options
    for employee_review in reviews:
      opinion_flags = employee_review.css('div.row.reviewBodyCell '+
        'span *::text').extract()
      opinion_dict = {
        'recommend':None,
        'outlook':None,
        'opinion':None
        }
      for opinion in opinion_flags:
        if 'Recommend' in opinion:
          opinion_dict['recommend'] = opinion
        elif 'Outlook' in opinion:
          opinion_dict['outlook'] = opinion
        elif 'CEO' in opinion:
          opinion_dict['opinion'] = opinion
        else:
          continue
      verbatim_comment_dict = {
        'Pros': None,
        'Cons': None,
        'Advice to Management': None
      }      

      verbatim_comments = employee_review.css('div.'+
        'v2__EIReviewDetailsV2__fullWidth')
      
      for comment in verbatim_comments:
        section = comment.css('p.strong.mb-0.mt-xsm::text').extract_first()
        value = (comment.css('p.v2__EIReviewDetailsV2__bodyColor::text')
          .extract_first())
        if section is not None:
          verbatim_comment_dict[section] = value
        else: 
          pass
      #if ceo_opinion_flag is not None:
      #  opinion_dict['opinion'] = ceo_opinion_flag + 'CEO'
      
      sub_star_ratings = (employee_review
        .css('span.gdBars.gdRatings.med::attr(title)').extract())

      review_item = GlassdoorReviewItem()

      review_item['search_name'] = self.company_name
      review_item['glassdoor_company_name']= (
        response.css('div.header.cell.info p.h1.strong.tightAll::text')
        .extract_first())
      review_item['summary']= (
        employee_review.css('.summary>a::text').extract_first()[1:-1])
      review_item['author_title']=(
        employee_review.css('span.authorJobTitle::text').extract_first())
      review_item['author_location']= (employee_review.
        css('span.authorLocation::text').extract_first())
      review_item['recommends_flag']=opinion_dict['recommend']
      review_item['outlook_flag']=opinion_dict['outlook']
      review_item['ceo_opinion_flag']=opinion_dict['opinion']
      review_item['main_text_description']= (
        employee_review.css('p.mainText::text').extract_first())
      review_item['pros_description']= verbatim_comment_dict['Pros']
      review_item['cons_description']= verbatim_comment_dict['Cons']
      review_item['advice_to_management_description'] = (
        verbatim_comment_dict['Advice to Management'])
      review_item['star_rating_overall']= (
        float(employee_review.css('span.value-title::attr(title)').extract_first()))
      review_item['star_rating_work_life_balance']= (
        float(sub_star_ratings[0]) if len(sub_star_ratings) >= 1 else None)
      review_item['star_rating_culture_and_values']= (
        float(sub_star_ratings[1]) if len(sub_star_ratings)>=2 else None)
      review_item['star_rating_career_opportunities']= (
        float(sub_star_ratings[2]) if len(sub_star_ratings)>=3 else None)
      review_item['star_rating_comp_and_benefits']= (
        float(sub_star_ratings[3]) if len(sub_star_ratings)>=4 else None)
      review_item['star_rating_senior_management']= (
        float(sub_star_ratings[4]) if len(sub_star_ratings)>=5 else None)
      review_item['review_date']= (
        employee_review.css('time.date::attr(datetime)').extract_first())

      # Return the review object for data processing
      yield review_item      

    # Find the pagination link and follow it to process the next set of reviews
    follow_link = response.css('li.pagination__PaginationStyle__next>a:'
      'not(.pagination__ArrowStyle__disabled)::attr(href)').extract_first()

    if follow_link is not None:
      self.custom_wait()
      yield scrapy.Request('https://www.glassdoor.co.uk'+follow_link
        ,cookies=self.cookies, callback = self.company_reviews_parse)
    

