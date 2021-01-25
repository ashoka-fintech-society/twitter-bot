from dotenv import load_dotenv; load_dotenv()
import tweepy
import requests
from bs4 import BeautifulSoup

import os
import json

#==============================================================================

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_KEY = os.getenv('ACCESS_KEY')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#==============================================================================

FILENAME = 'prevLinks.json'
prevLinks = json.load(open(FILENAME))

scrapeList = {
	'Forbes': ['https://www.forbes.com/search/?q=(loopTopic)&sort=recent', 'stream-item__title']
	}

#==============================================================================

def writeJSON(dictObject):

	with open(FILENAME, "w") as output:
		json.dump(dictObject, output, indent=2)

def web_source(link, anchorElemClass, limit):

	page = requests.get(link)
	soup = BeautifulSoup(page.content, 'html.parser')
	results = soup.findAll("a", {"class": anchorElemClass})[:limit] #restricting to X
	
	for anchorElem in results:
		tempLink = anchorElem['href']
		
		if tempLink not in prevLinks:
			tempTitle = anchorElem.string.strip().title()
			prevLinks[tempLink] = tempTitle
			#api.update_status(f'{tempTitle}\n{tempLink}')

def executeBlock():

	try:
		for topic in ['blockchain', 'fintech', 'cryptocurrency']:	
			for siteInfo in scrapeList.values():
				web_source(link=siteInfo[0].replace('(loopTopic)', topic), anchorElemClass=siteInfo[1], limit=3)
	except:
		pass
	finally:
		writeJSON(prevLinks)

executeBlock()
