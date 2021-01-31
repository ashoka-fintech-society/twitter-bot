from dotenv import load_dotenv; load_dotenv()
from TwitterAPI import TwitterAPI
import requests
from bs4 import BeautifulSoup
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

import os
import json

#==============================================================================

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN_KEY = os.getenv('ACCESS_TOKEN_KEY')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

#==============================================================================

scrapeList = {
	'Forbes': ['https://www.forbes.com/search/?q=(loopTopic)&sort=recent', 'stream-item__title']
	}

#==============================================================================

def web_source(link, anchorElemClass, limit, db, classObj):

	page = requests.get(link)
	soup = BeautifulSoup(page.content, 'html.parser')
	results = soup.findAll("a", {"class": anchorElemClass})[:limit] #restricting to X

	for anchorElem in results:
		tempLink = anchorElem['href']
		tempTitle = anchorElem.string.strip().title()

		try:
			newLink = classObj(title=tempTitle, link=tempLink)
			db.session.add(newLink)
			db.session.commit()
		except IntegrityError or UniqueViolation:
			db.session.rollback()
			continue

		r = api.request('statuses/update', {'status':f'{tempTitle}\n{tempLink}'})
		if r.status_code != 200:
			db.session.delete(newLink)
			db.session.commit()
			raise ArithmeticError

def executeBlock(databaseInstance, tableClass):

	try:
		for topic in ['blockchain', 'fintech', 'cryptocurrency']:	
			for siteInfo in scrapeList.values():
				web_source(link=siteInfo[0].replace('(loopTopic)', topic), anchorElemClass=siteInfo[1], limit=1, db=databaseInstance, classObj=tableClass)
	except ArithmeticError:
		return 500

	return 200
