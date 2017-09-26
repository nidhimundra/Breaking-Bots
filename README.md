# Breaking-Bots
Evaluating Websites’ Defenses against Web Crawlers

# Motivation
Global Internet traffic is growing at an estimated rate of 22% per year. However, the Web traffic is dominated by numerous bots crawling the web with different intents. A recent report by Imperva Incapsula reported that 52% of the Web traffic is just bots, and 28.9% among them are the “bad” ones, such as impersonators, scrapers, spammers and hacker tools! Thelwall M et al. Furthermore, even if a badly implemented “good” crawler crawls a middle-sized website, the website will slow down or be totally inaccessible. Because of such intentional or inadvertent effects of crawler activities, it is important to have robust crawler detection techniques in websites. 

Currently, three main methods are used to detect the Web crawlers:
* Log attributes detection method 
* Method based on trap technology 
* Method based on the web navigational patterns. 

# Goals of the project
The main goal of our project is to study websites’ responses to different requests from web crawlers. In this regard, we would like to explore different types of crawler behaviours such as time difference in two requests, a number of entry points to a website, with/without user-agent fields, multiple crawlers on a single website, etc.

Based on the responses from different websites to different HTTP requests from crawlers, we would like to identify possible similarities and differences in the mechanisms that the websites employ to detect and block web crawlers. Using the similarities and differences, we aim to classify these mechanisms for different websites and also classify the websites, in order to identify which mechanisms are good for a particular type of  website. 

To see the effect of crawler(s) on a website, if possible, we would like to measure different aspects of websites’ response such as response time to legitimate requests when crawler(s) is/are running. This might allow us to propose an optimum crawler detection strategy for a website.

