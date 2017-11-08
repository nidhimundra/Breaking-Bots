import logging
import csv
from selenium import webdriver
from urllib.parse import urldefrag, urljoin
from collections import deque
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display

class SeleniumCrawler(object):
 
    def __init__(self, base_url, exclusion_list, output_file='example.csv', start_url=None):
 
        display = Display(visible=0, size=(800, 600))
        display.start()

        assert isinstance(exclusion_list, list), 'Exclusion list - needs to be a list'
 
        self.browser = webdriver.Firefox()  #Add path to your Chromedriver
 
        self.base = base_url # To ensure that any links discovered during our crawl lie within the same domain/sub-domain
 
        self.start = start_url if start_url else base_url  # If no start URL is passed use the base_url
 
        self.exclusions = exclusion_list  #List of URL patterns we want to exclude e.g. ['?','signin','login']
 
        self.crawled_urls = []  #List to keep track of URLs we have already visited
 
        self.url_queue = deque([self.start])  #Add the start URL to our list of URLs to crawl
 
        self.output_file = output_file

   	def get_page(self, url):
        try:
            self.browser.get(url)
            return self.browser.page_source
        except Exception as e:
            logging.exception(e)
            return

    def get_soup(self, html):
        if html is not None:
            soup = BeautifulSoup(html, 'lxml')
            return soup
        else:
        	print "html is empty"
            return

    def get_links(self, soup):
 
        for link in soup.find_all('a', href=True): #All links which have a href element
            link = link['href'] #The actually href element of the link
            if any(e in link for e in self.exclusions): #Check if the link matches our exclusion list
                continue #If it does we do not proceed with the link
            url = urljoin(self.base, urldefrag(link)[0]) #Resolve relative links using base and urldefrag
            if url not in self.url_queue and url not in self.crawled_urls: #Check if link is in queue or already crawled
                if url.startswith(self.base): #If the URL belongs to the same domain
                    self.url_queue.append(url) #Add the URL to our queue