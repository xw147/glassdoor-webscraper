import pymongo

import json                                                                     
                                                                                
from glassdoor_robot.items import GlassdoorCompanyItem, GlassdoorReviewItem     
                                                                                
mongo_conf = None                                                               
with open("config.json") as config_file:                                        
  mongo_conf = json.load(config_file)['MongoDbConfig']                          
                                                                                
        
connection = pymongo.MongoClient(                                           
  mongo_conf['Server'],                                                     
  mongo_conf['Port']                                                        
)                                                                           
db = connection[mongo_conf['Database']]                                     
company_collection = db[mongo_conf['CompanyCollection']]               
review_collection = db[mongo_conf['ReviewCollection']]                 

def q(text, isString = 1, isLast = 0):
  string = ''
  if isString == 1:
    string += '"'
  string += str(text).replace('"',"'")
  if isString == 1:
    string += '"'
  if isLast == 0:
    string+=','
  return string

#output headers
print (
  q('company_name') +
  q('summary')+
  q('author_title')+
  q('author_location') + 
  q('recommends_flag') + 
  q('outlook_flag') + 
  q('ceo_opinion_flag') + 
  q('main_text_description') + 
  q('pros_description') + 
  q('cons_description') + 
  q('advice_to_management_description') + 
  q('star_rating_overall') + 
  q('star_rating_work_life_balance') + 
  q('star_rating_culture_and_values') + 
  q('star_rating_career_opportunities') + 
  q('star_rating_comp_and_benefits') + 
  q('star_rating_senior_management') + 
  q('star_rating_review_date',1,1)
)

for r in review_collection.find():
  print(
    q(r['search_name']) + 
    q(r['summary']) + 
    q(r['author_title']) + 
    q(r['author_location']) +
    q(r['recommends_flag']) +
    q(r['outlook_flag']) + 
    q(r['ceo_opinion_flag']) +
    q(r['main_text_description']) + 
    q(r['pros_description']) + 
    q(r['cons_description']) + 
    q(r['advice_to_management_description']) +
    q(r['star_rating_overall'],0) + 
    q(r['star_rating_work_life_balance'],0) +
    q(r['star_rating_culture_and_values'],0) +
    q(r['star_rating_career_opportunities'],0) +
    q(r['star_rating_comp_and_benefits'],0) + 
    q(r['star_rating_senior_management'],0) + 
    q(r['review_date'],1,1)
  )
               

