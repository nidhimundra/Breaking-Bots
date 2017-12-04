import os
import csv
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

# Change csv_filename to fetch data from some other CSV file
csv_filename = "top-500-urls"

# Change the request config to fetch configuration from some other python file
from request_config import *

# Import all the custom settings
from scrapy_settings import *

class BreakingBotsSpider(scrapy.Spider):
    name = "Breaking-bot"
    custom_settings = CUSTOM_SETTINGS
    visited_urls = []

    with open(csv_filename + ".csv", "rb") as f:
        urls = []
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            if "http" not in line[1]:
                urls.append("http://" + line[1])
            else:
                url.append(line[1])
        start_urls = urls
        visited_urls = start_urls

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse,
                                    errback=self.errback,
                                    method=METHOD,
                                    headers=HEADERS,
                                    body=BODY,
                                    cookies=COOKIES,
                                    meta=META,
                                    encoding=ENCODING,
                                    dont_filter=DONT_FILTER
                                    )

    def parse_recursively(self, response):
        self.parse(response)
        domain = response.url.split("//")[-1].split("/")[0].split('www.')[-1]
        extractor = LinkExtractor(allow_domains=domain)
        links = extractor.extract_links(response)
        for link in links:
            if link.url not in self.visited_urls:
                self.visited_urls.append(link.url)
                yield scrapy.Request(link.url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        yield {
            "url": response.url,
            "status": response.status,
            "flags": response.flags,
            "number_of_tags": len(soup.find_all(True)),
            "length": len(response.body),
            "error_message": "",
            "error_type": ""
        }
               
    def errback(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            yield {
                "url": response.url,
                "status": response.status,
                "flags": response.flags,
                "number_of_tags": 0,
                "length": 0,
                "error_message": "",
                "error_type": "HttpError"
            }
        elif failure.check(DNSLookupError):
            request = failure.request
            yield {
                "url": request.url,
                "status": "",
                "flags": [],
                "number_of_tags": 0,
                "length": 0,
                "error_message": "",
                "error_type": "DNSLookupError"
            }
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            yield {
                "url": request.url,
                "status": "",
                "flags": [],
                "number_of_tags": 0,
                "length": 0,
                "error_message": "",
                "error_type": "TimeoutError"
            }
        else:
            request = failure.request
            yield {
                "url": request.url,
                "status": "",
                "flags": [],
                "number_of_tags": 0,
                "length": 0,
                "error_message": "",
                "error_type": "Other"
            }
