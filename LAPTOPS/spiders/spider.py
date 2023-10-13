import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.spiders import Spider, Rule
from scrapy.linkextractors import LinkExtractor
from LAPTOPS.items import ProyectoScrapyItem

class LaptopSpider(scrapy.Spider):
    name = 'laptop'
    item_count = 0
    allowed_domains = ['www.loginstore.com']
    start_urls = ['https://www.loginstore.com/computacion/laptops/laptops']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//li[@class="item"]/div/a'))),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//h2[@class="ui-search-item__title"]')),
             callback='parse_item', follow=False),
    )

    @staticmethod
    def parse(response):
        ml_item = ProyectoScrapyItem()

        ml_item['titulo'] = response.xpath('//*[@id="product_addtocart_form"]/div[3]/div[1]/h1/text()').extract_first()
        ml_item['codigo'] = response.xpath('//*[@id="product_addtocart_form"]/div[3]/div[1]/p[1]/text()').extract_first()
        ml_item['descripcion'] = response.xpath('//*[@id="product_addtocart_form"]/div[3]/div[2]/div/text()').extract_first()
        ml_item['precio'] = response.xpath('//*[@id="product_addtocart_form"]/div[3]/div[3]/div/text()').extract_first()
        ml_item['stock'] = response.xpath('//*[@id="product_addtocart_form"]/div[3]/div[5]/span/text()').extract_first()
        ml_item['plazo'] = response.xpath('//*[@id="product_addtocart_form"]/div[3]/strong/text()').extract_first()

        LaptopSpider.item_count += 1
        if LaptopSpider.item_count > 20:
            raise CloseSpider('item_exceeded')
        yield ml_item
