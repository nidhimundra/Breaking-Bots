import logging, io, json, os, csv, requests
from selenium import webdriver
from urlparse import urldefrag, urljoin
from collections import deque
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from browsermobproxy import Server
from threading import Thread, Lock, Timer

mac_path = "/Users/Virat/Documents/UMass Code/653/Breaking-Bots/browsermob-proxy-2.1.4/bin/browsermob-proxy"
ubuntu_path = '/home/vshejwalkar/Documents/Breaking-Bots/browsermob-proxy-2.1.4/bin/browsermob-proxy'

ubuntu_dir = '/home/vshejwalkar/Documents/Breaking-Bots/'

class url(object):
    def __init__(self, url_name, url_depth):
        self.url_name = url_name
        self.url_depth = url_depth


class SeleniumCrawler(object):
 
    def __init__(self, base_url, exclusion_list, file_name_base, max_depth, timeout, start_url=None):
 
        assert isinstance(exclusion_list, list), 'Exclusion list - needs to be a list'
        
        self.server = Server(ubuntu_path)
        self.server.start()
        self.proxy = self.server.create_proxy()
        
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_proxy(self.proxy.selenium_proxy())

        # Add path to your Chromedriver
        self.browser = webdriver.Firefox(firefox_profile=self.profile)
        self.timeout = timeout
        self.browser.set_page_load_timeout(self.timeout)
        
        # To ensure that any links discovered during our crawl lie within the same domain/sub-domain
        self.base = base_url
 
        # If no start URL is passed use the base_url
        self.start = url(start_url, 0) if start_url else url(base_url, 0)

        # List of URL patterns we want to exclude e.g. ['?','signin','login']
        self.exclusions = exclusion_list
 
        # List to keep track of URLs we have already visited
        self.crawled_urls = []
 
        # Add the start URL to our list of URLs to crawl
        self.url_queue = deque([self.start])
 
        self.file_name_base = file_name_base
        
        self.dir_name = ubuntu_dir + file_name_base + '/'
        
        if not os.path.exists(self.dir_name):
            os.makedirs(self.dir_name)
        
        self.output_file = self.dir_name + file_name_base + '.csv'

        self.response_file = self.dir_name + file_name_base + '_responses.csv'
        with open(self.response_file, 'ab') as responsefile:
            writer = csv.writer(responsefile)
            data = ['url depth', 'primary url', 'primary url status code', 'redirected url if any', 'redirected url status code']
            writer.writerow(data)

        self.max_depth = max_depth

    def get_page(self, url):
        try:
            self.proxy.new_har(url.url_name)
            self.browser.get(url.url_name)
            redirectURL = ''
            redirectURL_entry = None
            har_info = json.dumps(self.proxy.har, indent=4)
            har = json.loads(har_info)

            if har.get('log').get('entries')[0].get('response').get('status') >= 300 and har.get('log').get('entries')[0].get('response').get('status') < 400:
                redirectURL = har.get('log').get('entries')[0].get('response').get('redirectURL')
                
                for i in range(len(har.get('log').get('entries'))):
                    if har.get('log').get('entries')[i].get('request').get('url') == redirectURL:
                        redirectURL_entry = i

            with open(self.response_file, 'ab') as responsefile:
                writer = csv.writer(responsefile)

                if redirectURL_entry:
                    data = [url.url_depth, url.url_name, har.get('log').get('entries')[0].get('request').get('url'), har.get('log').get('entries')[0].get('response').get('status'), har.get('log').get('entries')[redirectURL_entry].get('request').get('url'), har.get('log').get('entries')[redirectURL_entry].get('response').get('status')]
                else:
                    data = [url.url_depth, url.url_name, har.get('log').get('entries')[0].get('request').get('url'), har.get('log').get('entries')[0].get('response').get('status')]

                writer.writerow(data)

            # har_file = self.dir_name + self.file_name_base + '_' + str(len(self.crawled_urls)) +'.har'            
            # save_har = open(har_file,'a')
            # save_har.write(har_info)
            # save_har.close()
            return self.browser.page_source
        except Exception as e:
            logging.exception(e)
            with open(self.response_file, 'ab') as responsefile:
                writer = csv.writer(responsefile)
                data = [url.url_depth, url.url_name, 'Timeout - {}'.format(self.timeout)]
                writer.writerow(data)
            return

    def get_soup(self, html):
        if html is not None:
            soup = BeautifulSoup(html, 'lxml')
            return soup
        else:
            print "html is empty"
            return

    def get_links(self, soup, url_depth):
        if url_depth < self.max_depth:
            for link in soup.find_all('a', href=True): #All links which have a href element
                link = link['href'] #The actually href element of the link
                if any(e in link for e in self.exclusions): #Check if the link matches our exclusion list
                    continue #If it does we do not proceed with the link
                url_name = urljoin(self.base, urldefrag(link)[0]) #Resolve relative links using base and urldefrag
                url_found = False
                if url_name not in self.crawled_urls:
                    for i in range(len(self.url_queue)):
                        if url_name == self.url_queue[i].url_name: #Check if link is in queue or already crawled
                            url_found = True
                            break
                    if not url_found and url_name.startswith(self.base):
                        self.url_queue.append(url(url_name, (url_depth + 1))) #Add the URL to our queue
                else:
                    url_found = True
        else:
            pass
            # print "url depth {} not adding links to the queue".format(self.max_depth)
                    
    def get_data(self, soup):
        try:
            title = soup.find('title').get_text().strip().replace('\n','')
        except:
            title = None
        return title

    def csv_output(self, url, title):
 
        with open(self.output_file, 'ab') as outputfile:
            writer = csv.writer(outputfile)
            if title:
                data = [url.url_depth, url.url_name, title.encode('utf-8')]
            else:
                print "there is no title for the article"
                data = [url]
            writer.writerow(data)

    def run_crawler(self):
        display = Display(visible=0, size=(800, 600))
        display.start()

        # If we have URLs to crawl - we crawl
        while len(self.url_queue):
            # We grab a URL object from the left of the list
            current_url = self.url_queue.popleft()
            # We then add this URL object to our crawled list
            self.crawled_urls.append(current_url.url_name)

            html = self.get_page(current_url)

            # If the end URL is different from requested URL - add URL to crawled list
            # print self.browser.current_url, current_url.url_name
            if self.browser.current_url != current_url.url_name:
                self.crawled_urls.append(self.browser.current_url)
            
            soup = self.get_soup(html)

            # If we have soup - parse and write to our csv file
            if soup is not None:
                self.get_links(soup, current_url.url_depth)
                title = self.get_data(soup)
                self.csv_output(current_url, title)

        self.browser.quit()
        display.stop()

def extract_urls(csv_file):
    url_threads = []
    selenium_wnds = []
    exclusion_list = ['signin','login', '.pdf','.pptx','docx','mailto:']
    with open(csv_file + '.csv', 'rb') as f:
        reader = csv.reader(f)
        for i, line in enumerate(reader):
            url_name = "https://www." + line[1]
            selenium_wnds.append(SeleniumCrawler(url_name, exclusion_list, line[1], 2, 20))
            thread = Thread(name=line[1], target=selenium_wnds[i].run_crawler)
            thread.start()
            url_threads.append(thread)

extract_urls('top_100')