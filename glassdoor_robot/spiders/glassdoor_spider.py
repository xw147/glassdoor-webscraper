# Python Standards
import sys
import json
from time import sleep
from urllib.parse import urlencode
import random 
from selenium.webdriver.common.by import By
from pickle import NONE


driver_path = '/usr/local/bin/chromedriver'


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

starDict = {"css-s88v13" : "5", "css-1nuumx7" : "4", "css-vl2edp" : "3", "css-18v8tui" : "2", "css-xd4dom": "1"}
colorDict = {"css-hcqxoa" : "Recommended", "css-10xv9lv" : "No Review", "css-1kiw93k" : "Not Recommended", "css-1h93d4v" : "Moderate"}



class GlassdoorSpider(InitSpider):
  name = "glassdoor_spider"
  
    
  custom_settings = {
            'FEED_FORMAT': 'csv',
            'FEED_URI': '/Users/work/glassdoor-webscraper/glassdoor_robot/test1.csv'
   }
  

  def __init__(self, review_url, **kwargs):
    self.review_url = review_url
    self.cookies = None
    self.configuration = configuration
   
  def custom_wait(self):
    min_time = 5.0
    max_time = 10.0
    sleep(random.uniform(min_time,max_time))
    return True

  def init_request(self):   
    # Login to Glassdoor using Selenium
    ########### use chrmoe #########33
    # driver = webdriver.Firefox(executable_path="./drivers/geckodriver")
    driver = webdriver.Chrome(executable_path=driver_path)
    
    
    # driver.get("https://www.glassdoor.co.uk")
    # # Apply wait condition to prevent overloading the server with requests
    # self.custom_wait()    
    # # Submit login credentials into form
    # driver.find_element_by_class_name('sign-in').click()
    # self.custom_wait()
    # driver.find_element_by_name('username').send_keys(
    #   configuration["GlassdoorConfig"]["Username"])
    # self.custom_wait() 
    # driver.find_element_by_name('password').send_keys(
    #   configuration["GlassdoorConfig"]["Password"], Keys.ENTER)
    # # Store the authenticated cookies so they can be copied to scrapy
    # self.cookies = driver.get_cookies()
    # # Close the web browser
    # driver.quit()
    # self.custom_wait()    
    # # Generate request for the company search
    # form_data = {'sc.keyword': self.company_name}
    
    driver.get("https://www.glassdoor.co.in/profile/login_input.htm?userOriginHook=HEADER_SIGNIN_LINK")
    # Apply wait condition to prevent overloading the server with requests
    self.custom_wait()    
    # Submit login credentials into form
    
    driver.find_element(by=By.NAME, value='username').send_keys(
      configuration["GlassdoorConfig"]["Username"])
    self.custom_wait() 
    driver.find_element(by=By.NAME, value = 'password').send_keys(
      configuration["GlassdoorConfig"]["Password"], Keys.ENTER)
    # Store the authenticated cookies so they can be copied to scrapy
    self.cookies = driver.get_cookies()
    # Close the web browser
    driver.quit()
    self.custom_wait()   
    
     
    # Generate request for the company search
    # form_data = {'sc.keyword': self.company_name}
    # yield scrapy.Request(
    #   "https://www.glassdoor.co.uk/Reviews/company-reviews.htm?" + 
    #   urlencode(form_data), 
    #   cookies=self.cookies, 
    #   callback=self.auth_company_search_parse
    # )
    yield scrapy.Request(
      self.review_url, 
      cookies=self.cookies, 
      callback=self.company_reviews_parse
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
    ##### to be done ###########
    ######## add values to those options ######
    for employee_review in reviews:
        
        
      # opinion_flags = employee_review.css('div.row.reviewBodyCell '+
      #   'span *::text').extract()
      # opinion_dict = {
      #   'recommend':None,
      #   'outlook':None,
      #   'opinion':None
      #   }
      # for opinion in opinion_flags:
      #   if 'Recommend' in opinion:
      #     opinion_dict['recommend'] = opinion
      #   elif 'Outlook' in opinion:
      #     opinion_dict['outlook'] = opinion
      #   elif 'CEO' in opinion:
      #     opinion_dict['opinion'] = opinion
      #   else:
      #     continue
      
      
      recommends_labels = employee_review.css('div.d-flex.align-items-center.mr-std')
      recommends = {}
      for r in recommends_labels:
          category = r.css('span::text').extract_first()
          l = r.css('span::attr(class)').extract_first().split()[1] 
          recommends[category] = colorDict[l]  
          xxx = 1
          
      
      
      verbatim_comment_dict = {
        'Pros': None,
        'Cons': None,
        'Advice to Management': None
      }      

      verbatim_comments = employee_review.css('div.'+
        'v2__EIReviewDetailsV2__fullWidth')
      
      for comment in verbatim_comments:
        section = comment.css('p.mb-0.strong::text').extract_first()
        temp = (comment.css('p.mt-0.mb-0.pb.v2__EIReviewDetailsV2__bodyColor'))
        value = (temp.css('span::text').extract_first())
        if type(value) == str:
            value = value.replace('\r\n', ',')
        if section is not None:
          verbatim_comment_dict[section] = value
        else: 
          pass
      #if ceo_opinion_flag is not None:
      #  opinion_dict['opinion'] = ceo_opinion_flag + 'CEO'
      
      sub_labels = (employee_review.css('ul.pl-0 li'))
      sub_ratings = {}
      for s in sub_labels:
          category = s.css('div:nth-child(1)::text').extract_first()
          l = s.css('::attr(class)').extract_first().split()[0]
          sub_ratings[category] = starDict[l]
         
         
          

      review_item = GlassdoorReviewItem()
 
      # review_item['search_name'] = self.company_name
      # review_item['glassdoor_company_name']= (
      #   response.css('div.header.cell.info p.h1.strong.tightAll::text')
      #   .extract_first())
      
      title_and_date = employee_review.css('span.authorJobTitle::text').extract_first().split('-')
      review_item['review_date']= (title_and_date[0])
      review_item['employee_title']=(title_and_date[1])
      
      review_item['employee_location']= (employee_review.
        css('span.authorLocation::text').extract_first())
      
      review_item['employee_status'] =  (
          employee_review.css('div.d-flex.align-items-start.justify-content-between.pt-std.px-std>div>span::text').extract_first())
      
      
      review_item['review_title'] = employee_review.css('h2>a::text').extract_first()
      
      review_item['helpful_count'] = None
      review_text = employee_review.css('div.common__EiReviewDetailsStyle__socialHelpfulcontainer.pt-std::text').extract()
      if 'found this review' in review_text:
                str_list = review_text.text.split('\n')
                sub = 'people found this review helpful'
                for r in str_list:
                    if sub in r:
                        review_item['helpful_count'] = r[0]
                        break

      
      review_item['pros']= verbatim_comment_dict['Pros']
      review_item['cons']= verbatim_comment_dict['Cons']
      
      review_item['rating_overall']= (
        employee_review.css('span.ratingNumber.mr-xsm::text').extract_first())
      review_item['rating_balance']= (
        sub_ratings['Work/Life Balance'] if 'Work/Life Balance' in sub_ratings.keys() else None)
      review_item['rating_culture']= (
        sub_ratings['Culture & Values'] if 'Culture & Values' in sub_ratings.keys() else None)
      review_item['rating_diversity']= (
        sub_ratings['Diversity & Inclusion'] if 'Diversity & Inclusion' in sub_ratings.keys() else None)
      review_item['rating_career']= (
        sub_ratings['Career Opportunities'] if 'Career Opportunities' in sub_ratings.keys() else None)
      review_item['rating_comp']= (
        sub_ratings['Compensation and Benefits'] if 'Compensation and Benefits' in sub_ratings.keys() else None)
      review_item['rating_mgmt']= (
        sub_ratings['Senior Management'] if 'Senior Management' in sub_ratings.keys() else None)
      
      
      review_item['recommends']= (recommends['Recommend'] if 'Recommend' in recommends.keys() else None)
      review_item['positive_outlook']=(recommends['Business Outlook'] if 'Business Outlook' in recommends.keys() else None)
      review_item['approves_of_CEO']=(recommends['CEO Approval'] if 'CEO Approval' in recommends.keys() else None)
      
      # review_item['main_text_description']= (
      #   employee_review.css('p.mainText::text').extract_first())

      # review_item['advice_to_management_description'] = (
      #   verbatim_comment_dict['Advice to Management'])
      # review_item['star_rating_overall']= (
      #   float(employee_review.css('span.value-title::attr(title)').extract_first()))
      
      
      
    
      # Return the review object for data processing
      yield review_item      

    # Find the pagination link and follow it to process the next set of reviews
    # follow_link = response.css('li.pagination__PaginationStyle__next>a:'
    #   'not(.pagination__ArrowStyle__disabled)::attr(href)').extract_first()
    
    follow_link = response.css('head>link[rel="next"]::attr(href)').extract_first()
    
    if follow_link is not None:
      self.custom_wait()
      yield scrapy.Request(follow_link,cookies=self.cookies, callback = self.company_reviews_parse)
    

