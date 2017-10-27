import scrapy
import csv


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    with open("top-1000.csv", "rb") as f:
        urls = []
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            urls.append("http://www." + line[1])
        start_urls = urls

    def parse(self, response):
        yield {
            "url": response.url,
            "status": response.status
        }
        next_page = response.css('a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
