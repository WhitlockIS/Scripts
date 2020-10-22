import feedparser
import requests
import time
import datetime

while True:
	dallas_news_rss_url = 'http://www.fox4news.com/feeds/rssFeed?obfType=RSS_FEED&siteId=200007'
	feed = feedparser.parse(dallas_news_rss_url)
	print feed.entries[0].published + ' ' + feed.entries[0].title + ' ' + feed.entries[0].link
	print feed.entries[1].published + ' ' + feed.entries[1].title + ' ' + feed.entries[1].link
	
	feed_json = [{'title': feed.entries[0].title, 'link': feed.entries[0].link}, {'title': feed.entries[1].title, 'link': feed.entries[1].link}]
	feed_to_bvd = requests.post('http://<your BVD server>:12224/api/submit/<your API key>?tags=news, dallas', json=feed_json)
	
	print str(datetime.datetime.now()) + '\nSleeping for 30 seconds\n'
	time.sleep(30)
