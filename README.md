# Breaking-Bots
Evaluating Websites’ Defenses against Web Crawlers

# Motivation
Global Internet traffic is growing at an estimated rate of 22% per year. However, the Web traffic is dominated by numerous bots crawling the web with different intents. A recent report by Imperva Incapsula reported that 52% of the Web traffic is just bots, and 28.9% among them are the "bad" ones, such as impersonators, scrapers, spammers and hacker tools! Thelwall M et al. Furthermore, even if a badly implemented “good” crawler crawls a middle-sized website, the website will slow down or be totally inaccessible. Because of such intentional or inadvertent effects of crawler activities, it is important to have robust crawler detection techniques in websites. 

Web crawling technology is becoming extremely popular with our ever-increasing reliance on the Internet, especially on the search engines. Web crawlers (also known as spiders or bots) are essentially automated scripts trying to fetch data from the web in a systematic manner. To do this, web crawlers collect pages from the web and index them to support search engine queries. Many legit sites (such as Google and Bing) index downloaded pages to improve user experience by allowing users to find the pages faster.

When it comes to the World Wide Web there are both bad bots and good bots; there are crawlers with more sinister intentions. A recent report by Imperva Incapsula reported that 52\% of the Web traffic is just bots, and 28.9\% among them are the "bad" ones, such as impersonators, scrapers, spammers and hacker tools! Some of the effects of such crawlers are -- overloading the servers, very high bandwidth consumption, and unauthorized access to content. Because of such intentional or inadvertent effects of crawler activities, it is important to have robust crawler detection techniques in websites. Currently, three main methods are used to detect the Web crawlers:
* Log attributes detection method
* Method based on trap technology
* Method based on the web navigational patterns

In this regard, the aim of this project is to study websites’ responses to different requests sent from our configurable web crawler. Using top 100 websites from Cisco Umbrella 1 Million, a free list of most popular domains, we explored different crawler behaviors based on different User-Agent fields, different IP for different requests, time difference between two requests, number of concurrent requests, etc. We used Selenium - a headless browser to collect pages as a human would see; the aim is to juxtapose the responses that we got from our designed crawler. Based on the results from Scrapy crawler, we apply k-means clustering algorithm on features to categorize top websites into -- very highly defensive, highly defensive, defensive, poorly defensive and very poorly defensive websites.  Also, the project targets to use different proxies, with which crawler sends GET requests, to analyze their effect on the responses received from the websites.

How to run?
Steps:
1. Copy desired setting from settings/*.py to `scrapy_settings.py`
2. scrapy runspider crawler.py -o <Setting-Name>.json
3. python parse_json <Setting-Name>    // Note: - No extension here
4. See <Setting-Name>.csv to check results
