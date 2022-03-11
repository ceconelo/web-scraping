import scrapy
import re


class WjsSpiderSpider(scrapy.Spider):
    name = 'wjs'
    allowed_domains = ['wsj.com']
    start_urls = ['https://www.wsj.com/market-data/quotes/company-list/a-z/0-9']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for company in response.xpath('//table[@class="cl-table"]/tbody/tr'):
            url = company.xpath('./td[1]/a/@href').extract_first()
            slug = 'company-people'
            yield scrapy.Request(url=f'{url}/{slug}', callback=self.parse_profile)

        next_page = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_profile(self, response):
        exchange = None
        name = response.xpath('//span[@class="companyName"]/text()').extract_first()
        info_exchange = response.xpath('//span[@class="exchangeName"]/text()').extract_first()
        info_exchange = re.sub(r"[-()\"#/@;<>{}`+=~|.!?,]", "", info_exchange).split(':')
        print(f'Quantidade de itens: {len(info_exchange)}')
        if info_exchange:
            country = info_exchange[0]
        if len(info_exchange) > 1:
            exchange = info_exchange[1]
        description = response.xpath('//p[@class="txtBody"]/text()').extract_first()
        last_price = response.xpath('//span[@id="quote_val"]/text()').extract_first()
        w52_range = response.xpath('//div[@class="cr_data_field"]//*[contains(., "52 Week Range")]/following-sibling::span[1]/text()').extract_first()
        url = response.url

        yield {
            'Name' : name,
            'Country' : country,
            'Exchange' : exchange,
            'Description' : description,
            'Last Price' : last_price,
            '52 week range' : w52_range,
            'Url' : url
        }


