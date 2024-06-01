import scrapy
from scrapy.crawler import Crawler
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from time import sleep

class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["www.enfsolar.com"]
    start_urls = ["https://www.enfsolar.com/directory/installer/United%20States"]
    
    
    def parse(self, response):
        for name in response.xpath("//a[@class='w-[200px] inline-block mkjs-a']"):
            link = name.xpath("@href").get()
            yield response.follow(url=link,callback=self.data_parser)
            sleep(3)
            
        for page in range(8,12):
            pages = response.xpath("/html/body/div[2]/div/div/div[3]/div[2]/nav/ul/li[{}]/a/@href".format(page)).get()
            ab_url = response.urljoin(pages)
            yield response.follow(url=ab_url,callback=self.parse)
                        
    def data_parser(self,response):
        yield{
            "Company Name": response.xpath("//h1/text()").get(),
            "Address": response.xpath("//td[@itemprop='address']/text()").get(),
            "Phone": response.xpath("//td[@itemprop='telephone']/a/text()").get(),
            "Domain": response.xpath("//a[@itemprop='url']/text()").get(),
            "Country": response.xpath("(//tbody/tr/td[2]/text())[8]").get(),
            "Battery Storage": response.xpath("(//div[@class='col-xs-10 enf-section-body-content blue']/text())[1]").get(),
            "Installation size": response.xpath("(//div[@class='col-xs-10 enf-section-body-content blue']/text())[2]").get()
        }