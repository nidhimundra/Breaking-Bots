import scrapy
import csv

# Change csv_filename to fetch data from some other CSV file
csv_filename = "top-1000"

# Change config to fetch configuration from some other CSV file
from config import *

class BreakingBotsSpider(scrapy.Spider):
    name = "breaking-bots"

    with open(csv_filename + ".csv", "rb") as f:
        urls = []

        reader = csv.reader(f)
        for i, line in enumerate(reader):
            urls.append("http://www." + line[1])
        start_urls = urls

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, 
                method=METHOD,
                headers=HEADERS,
                body=BODY,
                cookies=COOKIES,
                meta=META,
                encoding=ENCODING,
                dont_filter=DONT_FILTER)

    def parse(self, response):
        yield {
            "url": response.url,
            "status": response.status
        }
        next_page = response.css('a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
