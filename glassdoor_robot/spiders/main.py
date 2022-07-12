
from scrapy.crawler import CrawlerProcess
from glassdoor_robot.spiders.glassdoor_spider import GlassdoorSpider





if __name__ == '__main__':
    # start spider from command line
#     scrapy.cmdline.execute(argv=['scrapy', 'crawl', 'winemag',
#                                  '-a', '-a start_page=1',
#                                  '-a', '-a end_page=1',
#                                   '-o', 'review.csv',
#                                  '-t', 'csv'])

# start spider 
    # test_url = 'https://www.glassdoor.co.uk/Reviews/Leeds-City-Council-Reviews-E305827.htm'
    test_url = 'https://www.glassdoor.co.uk/Reviews/LEEDS-Reviews-E1025428.htm'
    # test_url = 'https://www.glassdoor.co.uk/Reviews/NHS-Reviews-E12873.htm'
    
    process = CrawlerProcess()
    process.crawl(GlassdoorSpider, test_url)
    process.start()
    