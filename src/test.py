# import scrapy

# class StackOverflowSpider(scrapy.Spider):
#     name = 'stackoverflow'
#     start_urls = ['http://stackoverflow.com/questions?sort=votes']

#     def parse(self, response):
#         for href in response.css('.question-summary h3 a::attr(href)'):
#             full_url = response.urljoin(href.extract())
#             yield scrapy.Request(full_url, callback=self.parse_question)

#     def parse_question(self, response):
#         yield {
#             'title': response.css('h1 a::text').extract_first(),
#             'votes': response.css('.question .vote-count-post::text').extract_first(),
#             'body': response.css('.question .post-text').extract_first(),
#             'tags': response.css('.question .post-tag::text').extract(),
#             'link': response.url,
#         }

# class DoubanSpider(scrapy.Spider):
#     name = 'douban'
#     start_urls = ['https://book.douban.com/people/wubinwei/do']

#     def parse(self, response):
#         for href in response.css('a::attr(href)'):
#             full_url = response.urljoin(href.extract())
#             yield scrapy.Request(full_url, callback=self.parse_item)

#     def parse_item(self, response):
#         yield {
#             'title': response.css('h1 span::text').extract_first(),
#         }

# info_div = soup.find_all('div', class_='info')
# for div in info_div:
#     if not div.h2:
#         continue
#     title = " ".join(div.h2.text.split())
#     print(title)
#     splits = div.div.text.split('/')
#     author = splits[0].strip()
#     author2 = splits[1].strip()
#     publishor = splits[2].strip()
#     publish_date = splits[3].strip()
#     print(author)
#     print(author2)
#     print(publishor)
#     print(publish_date)
#     print()

