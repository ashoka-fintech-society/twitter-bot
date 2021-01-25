from dotenv import load_dotenv; load_dotenv()
import os

import tweepy
import requests
from bs4 import BeautifulSoup
import time

#==============================================================================
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_KEY = os.getenv('ACCESS_KEY')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
#==============================================================================
FILENAME = 'prev_link.txt'
#==============================================================================


i = 100


def retreive_prev_link(filename):
	f_read = open(filename, 'r')
	prev_link = f_read.read()
	f_read.close()
	return prev_link

def save_prev_link(prev_link, filename):
	f_write = open(filename, 'a')
	f_write.write(prev_link)
	f_write.write('\n')
	f_write.close()
	return


def web_source(link, search_term):
	page = requests.get(link)

	soup = BeautifulSoup(page.content, 'html.parser')

	results = soup.find(search_term)

	bot_prev_link = retreive_prev_link(FILENAME)

	bot_link = results.find('a')['href']
	bot_title = results.find('a')

	if bot_link not in bot_prev_link:
		print(bot_title.text.strip(), bot_link, sep = '\n') 
		#api.update_status('{} \n{}'.format(bot_title.text.strip(), bot_link))
		save_prev_link(bot_link, FILENAME)

		
for i in range(1):	
	web_source('https://www.forbes.com/search/?q=fintech&sort=recent&sh=39e5be9c279f', 'class_ = "stream-item__text"' )
	#web_source('https://www.forbes.com/search/?q=cryptocurrency&sort=recent&sh=39e5be9c279f', 'stream-item__text')



#Blockchain, payment systems, lending


#Twitter Info
#Bearer token = AAAAAAAAAAAAAAAAAAAAAKvcLQEAAAAAft4sQcthuCzTrWOEv4bcgN5FIFM%3DhSxFKp6AdUaaiosPf2UkdMYMvb7kcxhxQd74JhYyOAJvpbFjp4

#page = requests.get('https://www.investopedia.com/search?q=fintech')

#	soup = BeautifulSoup(page.content, 'html.parser')

#	results = soup.find(id= "search-results__list_1-0")

#	bot_link = results.find('a')['href']
#	bot_title = results.find('h3')

#	if bot_prev_link != bot_link:
#		print(bot_title.text.strip(), bot_link, sep = '\n') 
#		api.update_status('{} \n{}'.format(bot_title.text.strip(), bot_link))
#		bot_prev_link = bot_link
#	else:
#		continue 
	#Time delay in repeating the check
#	time.sleep(10)
