import requests
from bs4 import BeautifulSoup
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from google.cloud import storage

from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import concurrent.futures 
import threading
import csv



def output_csv(url, merchant_name, username, rating, total_review, total_sold, last_active, followers,
		following, description, instagram, facebook, twitter, linkedin, youtube, website): # create csv file and save data
	#sds_product_name, publish_date, revision_date, manufacturer_name, hcode = pdf_data(pdf_path)



	print("adding product data info in csv file...")
	# today_date 	= today()
	filename 	= "depop-new.csv"


	file_exists = os.path.isfile(filename)
	header = ['url', 'merchant_name','username','rating', 'total_review', 'total_sold', 'last_active',
		'followers', 'following', 'description','instagram', 'facebook', 'twitter','linkedin', 
		'youtube','merchant_site']


	with open(filename, 'a', encoding="utf-8-sig") as csvfile:
		writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n',fieldnames=header)
		
		if not file_exists:
			writer.writeheader()
		writer.writerow({
			'url': url, 'merchant_name': merchant_name, 'username': username, 'rating': rating,
			'total_review': total_review, 'total_sold': total_sold, 'last_active': last_active,
			'followers': followers, 'following': following, 'description':description,'instagram': instagram, 
			'facebook': facebook,'twitter': twitter, 'linkedin': linkedin, 'youtube': youtube,
			'merchant_site': website
        })
		print("sds info added in csv, going for next sds..")


def get_driver():
	options = webdriver.ChromeOptions()
	user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'    
	options.add_argument('user-agent={0}'.format(user_agent))
	options.add_argument('headless')
	options.add_argument("--window-size=1920,1080")
	options.add_argument("--no-sandbox")
	# options.add_argument("--disable-extensions")
	# options.add_argument("--dns-prefetch-disable")
	# options.add_argument("--disable-gpu")
	driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
	driver.set_page_load_timeout(120)
	driver.execute_script("return navigator.userAgent")

	return driver

# time.sleep(10)


def merchant_details(url):
	#url 		= 'https://www.depop.com/hunnybuncloset/'
	response 	= requests.get(url)
	time.sleep(1.5)
	soup 		= BeautifulSoup(response.text, features='html.parser')

	merchant_name 	= soup.find('h1', {'class': 'styles__FullName-aljd70-3'})
	if merchant_name:
		merchant_name = merchant_name.text
	print(merchant_name)

	username 		= soup.find('p', {'data-testid': 'username'})
	if username:
		username = username.text
	print(username)

	rating 	= ''
	feedback 		= soup.find('button', {'class': 'styles__FeedbackContainer-y0r7uh-0'})
	if feedback:
		rating 	= feedback.get('aria-label')

	print(rating)
	total_review 	= soup.find('span', {'class': 'styles__FeedbackNumber-y0r7uh-1'})
	if total_review:
		total_review = total_review.text
	print(total_review)

	sold_div 		= soup.find('div', {'data-testid': 'signals__sold'})
	total_sold = ''

	if sold_div:
		total_sold 	= sold_div.find('span')
		if total_sold:
			total_sold = total_sold.text
	print(total_sold)

	active_div 		= soup.find('div', {'data-testid': 'signals__active'})
	last_active 	= ''

	if active_div:
		last_active 	= active_div.find('span')
		if last_active:
			last_active = last_active.text
	print(last_active)

	followers 	= soup.find('button', {'aria-label': 'followers'})
	if followers:
		followers = followers.text


	print(followers)

	following 	= soup.find('button', {'aria-label': 'following'})
	if following:
		following = following.text
	print(following) 

	description = ''
	instagram 	= ''
	facebook 	= ''
	twitter 	= ''
	linkedin 	= ''
	youtube 	= ''
	website 	= ''

	description_div = soup.find('div', {'class': 'styles__UserDescription-aljd70-7'})
	if description_div:
		description 	= description_div.text
		all_link		= description_div.find_all('a')
		if all_link:
			for l in all_link:
				link = l.get('href')
				if 'instagram' in link:
					instagram 	= link
				elif 'facebook' in link:
					facebook 	= link
				elif 'twitter' in link:
					twitter 	= link
				elif 'linkedin' in link:
					linkedin 	= link
				elif 'youtube' in link:
					youtube 	= link
				else:
					website 	= link

	print(description)
	print(instagram)
	print(youtube)
	print(facebook)
	print(twitter)
	print(linkedin)
	output_csv(url, merchant_name, username, rating, total_review, total_sold, last_active, followers,
		following, description, instagram, facebook, twitter, linkedin, youtube, website)


# merchant_details()

def product_page(url):
	#url 		= 'https://www.depop.com/products/mattyjones2001-nike-react-element-55-no/'
	response 	= requests.get(url)
	soup 		= BeautifulSoup(response.text, features='html.parser')


	merchant_link 	= soup.find('a', {'data-testid': 'bio__username'})
	if merchant_link:
		merchant_link = merchant_link.get('href')
		merchant_link = 'https://www.depop.com{}'.format(merchant_link)
		merchant_details(merchant_link)




# product_page('https://www.depop.com/products/drip124sorceror-mens-canada-goose-expedition-parka/')
def product_list(driver):
	url 		= 'https://www.depop.com/search/?q='
	
	driver.get(url)
	time.sleep(4)
	html 		= driver.execute_script("return document.documentElement.outerHTML")
	soup 		= BeautifulSoup(html, features='html.parser')

	a = 1
	i = 0
	x = 0
	while a == 1:
		print("Scrolling...")
		body = driver.find_element_by_css_selector('body')
		body.send_keys(Keys.PAGE_DOWN)
		time.sleep(2)

		html 		= driver.execute_script("return document.documentElement.outerHTML")
		soup 		= BeautifulSoup(html, features='html.parser')

		products 	= soup.find_all('a', {'data-testid': 'product__item'})
		print(len(products))
		for p in products[x:]:
			i = i+1
			print(i)
			product_link 	= p.get('href')
			print(product_link)
			username 		= product_link.split('/products/')
			username 		= username[1].split('-')
			username   		= username[0]
			username 		= '@' + username

			with open('depop-new.csv', 'r', encoding ='utf-8-sig') as csvfile:
				csvreader = csv.reader(csvfile, delimiter=',')
				found = False
				for row in csvreader:
					if username == row[2]:
						found = True
			
			if found == False:
				product_link = 'https://www.depop.com{}'.format(product_link)
				product_page(product_link)
			else:
				print('This merchant already exist...')
		x = i

driver 	= get_driver()
product_list(driver)



