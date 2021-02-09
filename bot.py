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

def tweetFunc(idList, db, classObj):

	tweetList = classObj.query.filter(classObj.id.in_(idList)).all()
	success = list()

	for x in tweetList:

		r = api.request('statuses/update', {'status':f'{x.title}\n{x.link}'})

		if r.status_code != 200:

			classObj.query.filter(classObj.id.in_(list(set(idList) - set(success)))).delete()
			db.session.commit()
			return 500

		else:
			x.tweeted = True
			success.append(x.id)
	
	db.session.commit()
	return 200

def executeBlock(db, classObj, limit=2):

	resultDict = []

	try:
		for topic in ['fintech', 'cryptocurrency']:	
			for siteInfo in scrapeList.values():

				link = siteInfo[0].replace('(loopTopic)', topic)
				anchorElemClass = siteInfo[1]
		
				page = requests.get(link)
				soup = BeautifulSoup(page.content, 'html.parser')
				results = soup.findAll("a", {"class": anchorElemClass})[:limit]

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

					resultDict.append({"id":newLink.id, "title":tempTitle})

	except:
		return 500

	return resultDict