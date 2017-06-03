from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from quora_links.items import Question


class MySpider(CrawlSpider):
    name = 'quora'
    allowed_domains = ['quora.com']
    start_urls = ['https://www.quora.com/sitemap/questions?page_id=30']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('page_id'))),
        Rule(LinkExtractor(deny=('https://www.quora.com$', 'sitemap', 'answer', 'questions', 'robots')), callback='parse_item'),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is a question page! %s', response.url)
        # print(response)
        item = Question()
        # print(response.xpath('//span[@class="TopicNameSpan TopicName"]/text()').extract())
        item['topic'] = response.xpath('//span[@class="TopicNameSpan TopicName"]/text()').extract()
        # print(item['topic'])
        item['q'] = response.xpath('//h1//text()').extract()
        # print(item['q'])
        item['a'] = response.xpath('//div[@class="layout_2col_main"]/div[5]//*[contains(@class,"qtext")]//text()').extract()
        # print(item['a'])
        # item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        # item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
        # item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
        return item
