import os
import csv
import scrapy
from urlparse import urlparse
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

    # output_file = open("output" + ".csv", "wb")
    # output_writer = csv.writer(output_file)
    # output_writer.writerow(["Domain", "URL", "Length", "Number of Tags"])

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse_recursively,
                                    errback=self.errback,
                                    method=METHOD,
                                    headers=HEADERS,
                                    body=BODY,
                                    cookies=COOKIES,
                                    meta=META,
                                    encoding=ENCODING,
                                    dont_filter=DONT_FILTER
                                    )

    def _remove_attrs(self, soup):
        for tag in soup.findAll(True): 
            tag.attrs = None
        return soup

    def parse_recursively(self, response):
        self.parse(response)
        domain = response.url.split("//")[-1].split("/")[0].split('www.')[-1]
        # soup = BeautifulSoup(response.body, 'lxml')
        # # self.write_on_csv(domain, domain, soup, response)

        # clean_soup = soup
        # # clean_soup = self._remove_attrs(soup)
        # [s.extract() for s in soup('script')]
        # [s.extract() for s in soup('style')]
        # [s.extract() for s in soup('meta')]
        # print len(clean_soup.find_all(True))
        # html = clean_soup.prettify("utf-8")

        # content = ""
        # tags = [tag.name for tag in clean_soup.find_all()]
        # for tag in tags:
        #     content += "\n" + soup.find(tag).getText()
        # output_file = open("Output.txt", "wb")
        # output_file.write(content.encode('utf-8'))

        # if not os.path.exists("output_pages/" + domain):
        #     os.makedirs("output_pages/" + domain)
        # filename = response.url.split("/")[-1]
        # if filename == "":
        #     filename = "index.html"
        # with open("output_pages/" + domain + "/" + filename, 'wb') as f:
        #     f.write(response.body)
        # f.close()

        extractor = LinkExtractor(allow_domains=domain)
        links = extractor.extract_links(response)
        for link in links:
            if link.url not in self.visited_urls:
                self.visited_urls.append(link.url)
                yield scrapy.Request(link.url, callback=self.parse)

    def parse(self, response):
        yield {
            "url": response.url,
            "status": response.status
        }
        # referer = response.request.headers.get('Referer', None)
        # domain = referer.split("//")[-1].split("/")[0].split('www.')[-1]
        # soup = BeautifulSoup(response.body, 'lxml')
        # self.write_on_csv(domain, response.url, soup, response)
        # if not os.path.exists("output_pages/" + domain):
        #     os.makedirs("output_pages/" + domain)
        # filename = response.url.split("/")[-1]
        # if filename == "":
        #     filename = "index.html"
        # with open("output_pages/" + domain + "/" + filename, 'wb') as f:
        #     f.write(response.body)
        # f.close()

       
    def write_on_csv(self, domain, url, soup, response):
        print "-------", len([tag.name for tag in soup.find_all(True)])
        self.output_writer.writerow([domain, url, 1, len(soup.find_all(True))])
        
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
