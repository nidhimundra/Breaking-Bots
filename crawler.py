import os
import csv
import scrapy
from urlparse import urlparse
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

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
            urls.append("http://" + line[1])
            break
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

    def parse(self, response):
        yield {
            "url": response.url,
            "status": response.status
        }
        parsed_uri = urlparse(response.url)
        domain = '{uri.netloc}/'.format(uri=parsed_uri)

        if not os.path.exists("output_pages/" + domain):
            os.makedirs("output_pages/" + domain)

        filename = response.url.split("/")[-1]
        if filename == "":
            filename = "index.html"
        with open("output_pages/" + domain + "/" + filename, 'wb') as f:
            f.write(response.body)

        f.close()
        # Uncomment to scrape recursively
        next_page = response.css('a::attr(href)').extract_first()
        print "---------", next_page
        if next_page is not None and (response.url in next_page or "http" not in next_page):
            next_page = response.urljoin(next_page)
            if next_page not in self.visited_urls:
                self.visited_urls.append(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
    
    def errback(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            yield {
                "url": response.url,
                "status": response.status,
                "type": "HttpError"
            }
        elif failure.check(DNSLookupError):
            request = failure.request
            yield {
                "url": request.url,
                "type": "DNSLookupError"
            }
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            yield {
                "url": request.url,
                "type": "TimeoutError"
            }
        else:
            request = failure.request
            yield {
                "url": request.url,
                "reason": repr(failure),
                "type": "Other"
            }
