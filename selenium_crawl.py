import logging, io, json, os, csv
from selenium import webdriver
from urlparse import urldefrag, urljoin
from collections import deque
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from browsermobproxy import Server

mac_path = "/Users/Virat/Documents/UMass Code/653/Breaking-Bots/browsermob-proxy-2.1.4/bin/browsermob-proxy"
ubuntu_path = '/home/vshejwalkar/Documents/Breaking-Bots/browsermob-proxy-2.1.4/bin/browsermob-proxy'

ubuntu_dir = '/home/vshejwalkar/Documents/Breaking-Bots/'

class url(object):
    def __init__(self, url_name, url_depth):
        self.url_name = url
        self.url_depth = url_depth


class SeleniumCrawler(object):
 
    def __init__(self, base_url, exclusion_list, file_name_base, start_url=None):
 
        assert isinstance(exclusion_list, list), 'Exclusion list - needs to be a list'
        
        self.server = Server(ubuntu_path)
        self.server.start()
        self.proxy = self.server.create_proxy()
        
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_proxy(self.proxy.selenium_proxy())

        self.browser = webdriver.Firefox(firefox_profile=self.profile)  #Add path to your Chromedriver
        self.browser.set_page_load_timeout(8)
        self.base = base_url # To ensure that any links discovered during our crawl lie within the same domain/sub-domain
 
        self.start = start_url if start_url else base_url  # If no start URL is passed use the base_url
 
        self.exclusions = exclusion_list  #List of URL patterns we want to exclude e.g. ['?','signin','login']
 
        self.crawled_urls = []  #List to keep track of URLs we have already visited
 
        self.url_queue = deque([self.start])  #Add the start URL to our list of URLs to crawl
 
        self.file_name_base = file_name_base
        self.dir_name = ubuntu_dir + file_name_base + '/'
        if not os.path.exists(self.dir_name):
            os.makedirs(self.dir_name)
        self.output_file = self.dir_name + file_name_base + '.csv'

    def get_page(self, url):
        try:
            self.proxy.new_har(url)
            self.browser.get(url)
            har_info = json.dumps(self.proxy.har, indent=4)
            har_file = self.dir_name + self.file_name_base + '_' + str(len(self.crawled_urls)) +'.har'
            save_har = open(har_file,'a')
            save_har.write(har_info)
            save_har.close()
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
                self.url_queue.append(url) #Add the URL to our queue
            else:
                pass

    def get_data(self, soup):
        try:
            title = soup.find('title').get_text().strip().replace('\n','')
        except:
            title = None
        return title

    def csv_output(self, url, title):
 
        with open(self.output_file, 'ab') as outputfile:
            writer = csv.writer(outputfile
)            if title:
                data = [url, title.encode('utf-8')]
            else:
                print "there is no title for the article"
                data = [url]
            writer.writerow(data)

    def run_crawler(self):
        display = Display(visible=0, size=(800, 600))
        display.start()
        
        while len(self.url_queue): #If we have URLs to crawl - we crawl
            current_url = self.url_queue.popleft() #We grab a URL from the left of the list

            self.crawled_urls.append(current_url) #We then add this URL to our crawled list
            
            html = self.get_page(current_url)

            if self.browser.current_url != current_url: #If the end URL is different from requested URL - add URL to crawled list
                self.crawled_urls.append(current_url)
            
            soup = self.get_soup(html)
            # print soup
            if soup is not None:  #If we have soup - parse and write to our csv file
                self.get_links(soup)
                title = self.get_data(soup)
                self.csv_output(current_url, title)

        self.browser.quit()
        display.stop()

def extract_urls(csv_file):
    urls = []
    with open(csv_file + '.csv', 'rb') as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            url_name = "http://www." + line[1]
            # Create url objects with depth 0 and crawled = False
            urls.append(url(url_name, 0))

extract_urls('top-100')
# base_url = 'https://www.amazon.com/'
# exclusion_list = ['signin','login', '.pdf','.pptx','docx','mailto:']
# selenium_crawl = SeleniumCrawler(base_url, exclusion_list, 'amazon')
# selenium_crawl.run_crawler()