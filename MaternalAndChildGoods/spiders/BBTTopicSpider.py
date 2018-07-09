import scrapy
import re
from MaternalAndChildGoods.items import Topic

class BBTTopicSpider(scrapy.Spider):
    name = "BBTTopicSpider"
    # once <item_limit> items are collected, the spider closes
    item_limit = 1000
    item_count = 0
    # only url under <allowed_domains> will be scrapeds
    allowed_domains = ['http://www.babytree.com']
    # This is the list of starting websites 
    start_urls = [
        'http://www.babytree.com/community/yuer/',
        'http://www.babytree.com/community/xinqing/',
        'http://www.babytree.com/community/sheying/',
        'http://www.babytree.com/community/meishi/',
        'http://www.babytree.com/community/group39963/',
        'http://www.babytree.com/community/yuedu/',
        'http://www.babytree.com/community/dabenying/',
        'http://www.babytree.com/community/zaojiao/',
    ]
    
    def parse(self, response):
        
        # generate a selector
        selector = scrapy.Selector(response)

        # not flexible and portable
        topic_tag = re.findall(r'.*www\.babytree\.com/community/([^/]+)/.*',response.url)[0]

        # extract topics and info we want
        for topic_line in selector.xpath('//table[@class="groupForum"]//tr'):
            try:
                topic = Topic()
                topic['cls_tag'] = 2
                topic['ttext'] = ''.join(topic_line.xpath('td[@class="topicTitle"]/span/a/text()').extract())
                topic['href'] = topic_line.xpath('td[@class="topicTitle"]/span/a/@href').extract_first()
                topic['view_cnt'] = int(topic_line.xpath('td[@class="topicStat"]/span[@class="topicViews"]/text()').extract_first())
                topic['reply_cnt'] = int(topic_line.xpath('td[@class="topicStat"]/span[@class="topicReplies"]/text()').extract_first())
                author_and_time = ''.join(topic_line.xpath('td[@class="topicTime"]/span//text()').extract())
                topic['time'] = re.findall(r'\d+-\d+-\d+',author_and_time)[-1]
                # under test
                topic['tag'] = topic_tag

                self.item_count += 1
                yield topic
            except Exception as e:
                print(e)

        # extract next page request
        next_page = selector.xpath('//div[@class="pagejump"]/a[contains(text(),"下一页")]/@href').extract_first()
        
        if next_page is not None and self.item_count < self.item_limit:
            yield response.follow(next_page, callback=self.parse)