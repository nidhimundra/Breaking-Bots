import requests
import csv
from bs4 import BeautifulSoup

def crawl(url):
	print(url)
	r  = requests.get("http://www." + url)
	data = r.text
	soup = BeautifulSoup(data)
	for link in soup.find_all('a'):
		print(link.get('href'))

with open("top-1000.csv", "rb") as f:
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        crawl(line[1])