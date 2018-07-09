import scrapy
import re
from MaternalAndChildGoods.items import ImageUrl
from MaternalAndChildGoods.items import Text

class BBTContentSpider(scrapy.Spider):
    name = "BBTContentSpider"
    # once <item_limit> items are collected, the spider closes
    item_limit = 1000
    item_count = 0
    # only url under <allowed_domains> will be scrapeds
    allowed_domains = ['http://www.babytree.com']
    # This is the list of starting websites

    def start_requests(self):
        # urls = [
        #     'http://www.babytree.com/community/yuer/',
        #     'http://www.babytree.com/community/xinqing/',
        #     'http://www.babytree.com/community/sheying/',
        #     'http://www.babytree.com/community/meishi/',
        #     'http://www.babytree.com/community/group39963/',
        #     'http://www.babytree.com/community/yuedu/',
        #     'http://www.babytree.com/community/dabenying/',
        #     'http://www.babytree.com/community/zaojiao/',
        # ]
        urls = ['http://www.babytree.com/community/sheying/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_index)

    # parse forum index page  
    def parse_index(self, response):

        # generate a selector
        selector = scrapy.Selector(response)

        # extract all posts' links in one index page and generate requests
        for topic_line in selector.xpath('//table[@class="groupForum"]//tr'):
            try:
                post_link = topic_line.xpath('td[@class="topicTitle"]/span/a/@href').extract_first()
                yield response.follow(post_link, callback=self.parse_post)

            except Exception as e:
                print(e)

        # extract next index page's request
        next_page = selector.xpath('//div[@class="pagejump"]/a[contains(text(),"下一页")]/@href').extract_first()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_index)

        # parse one post page in the forum
    def parse_post(self, response):

        # generate a selector
        selector = scrapy.Selector(response)

        # extract topic of certain texts
        topic = selector.xpath('//table[@id="DivHbbs"]//h1/text()').extract_first().strip()

        # extract:
        # 1. text of every single post/reply
        # 2. informative pictures in a single post (emoji excluded)
        for post in selector.xpath('//div[@class="clubTopicSinglePost"]'):

            # extract one text item
            text = Text()
            text['cls_tag'] = 0
            post_time = re.findall(
                r'\d+-\d+-\d+\s\d+:\d+:\d+',
                ''.join(post.xpath('div//p[@class="postTime"]//text()').extract()))[0]

            text['time'] = post_time
            # Since topic content and reply content are formed in different ways
            # we need to judge which type of text it is

            # if the single post is a reply post 
            if not post.xpath('div//p[@id="topic_content"]'):
                text['text'] = ''.join(post.xpath('div//div[@class="postContent"]/text()').extract()).strip()
                content_box = post.xpath('div//div[@class="postContent"]')

            # if the single post is a topic post
            else:
                text['text'] = ''.join(post.xpath('div//p[@id="topic_content"]/text()').extract()).strip()
                content_box = post.xpath('div//p[@id="topic_content"]')

            text['topic'] = topic
            self.item_count += 1
            yield text

            # create ImageUrl item if there exists informative figures
            for img_url in content_box.xpath('img[not(@class)]/@data-original').extract():
                item = ImageUrl()
                item['cls_tag'] = 1
                item['time'] = post_time
                item['src'] = img_url
                self.item_count += 1
                yield item

        # generate request of next page
        next_page = response.xpath('//div[@class="nav-extra"]//a[contains(text(),"下一页")]/@href').extract_first()
        if next_page is not None and self.item_count < self.item_limit:
            yield response.follow(next_page, callback=self.parse_post)