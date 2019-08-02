# –––––––––––––––––––––––––––––––––––––––––––––––––––– * MARS WEB SCRAPING * –––––––––––––––––––––––––––––––––––––––––––––––––––– #
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import shutil
import pandas as pd
import time

from IPython.display import Image, display, HTML  # for printing to console;


def init_browser():
	executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
	return Browser("chrome", **executable_path, headless=False)


def scrape_info():
	browser = init_browser()
	# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– #
	# ### Visit [Nasa's Mars News website](https://mars.nasa.gov/news/) & retrieve the latest article's title & text
	# Start @ Nasa Mars News Homepage
	nasa_news_home = "https://mars.nasa.gov/news/"
	browser.visit(nasa_news_home)
	# goal: Parse news page to find title & paragraph of latest news article;
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	# Take out the <div> of name and get its value
	article_title = soup.find(attrs={'class': 'content_title'}).text.strip()
	article_paragraph = soup.find(
		attrs={'class': 'article_teaser_body'}).text.strip()
	# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– #
	# ### Visit [The Jet Propulsion Laboratory's Homepage](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)&
	# extract the featured image
	# Start @ JPL Homepage
	# browser = Browser("chrome", **executable_path, headless=False)
	jpl_home = "https://www.jpl.nasa.gov"
	image_thumb_url = jpl_home + "/spaceimages/?search=&category=Mars"
	browser.visit(image_thumb_url)
	# On JPL Homepage, automate clicking on 'FULL IMAGE' button;
	time.sleep(1)
	xpath = '//*[@id="full_image"]'
	results = browser.find_by_xpath(xpath)
	img = results[0]
	img.click()
	# On Full Image Page, automate clicking on 'more info' button;
	time.sleep(1)
	xpath = '//*[@id="fancybox-lock"]/div/div[2]/div/div[1]/a[2]'
	results = browser.find_by_xpath(xpath)
	img = results[0]
	img.click()
	# goal: Parse more info page to find image url;
	time.sleep(1)  # to ensure html fully loaded.
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	# HTML ABOVE INSPECTED & NARROWED DOWN
	# SELECTOR: page > section.content_page.module > div > article > figure > a
	img_rel_path = soup.figure.a['href']
	featured_img_url = jpl_home + img_rel_path
	# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– #
	# ### Retrieve latest tweet from the [Mars Weather Report's feed](https://twitter.com/marswxreport)<br>
	# Start @ Twitterfeed
	# browser = Browser("chrome", **executable_path, headless=False)
	mwr_twitter_home = "https://twitter.com/marswxreport"
	browser.visit(mwr_twitter_home)
	# goal: Parse html to pinpoint contents of latest tweet;
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	# HTML ABOVE INSPECTED & NARROWED DOWN
	mars_weather = soup.find(attrs={'class': 'TweetTextSize'}).text.strip()
	mars_weather = mars_weather.split(sep='pic.twitter.com')[0]
	# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– #
	# ### Retrieve the complete Mars table from the [Space Facts website](http://space-facts.com/mars/)<br>
	# Start @ Space Facts Website
	# browser = Browser("chrome", **executable_path, headless=False)
	space_facts_home = "https://space-facts.com/mars/"
	browser.visit(space_facts_home)
	# goal: use pandas to Parse & extract table;
	html = browser.html
	mars_table_df = pd.read_html(html)
	mars_table_df = mars_table_df[1]
	mars_table_df.columns = ['Attribute', 'Details']
	mars_table_df.set_index('Attribute', inplace=True)
	mars_table_df[:][:]
	# save df to html file & remove new line characters
	mars_table_df.to_html('current_files/mars_table.html'.replace('\n', ''))
	mars_table_html = mars_table_df.to_html()
	to_replace = '<thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>Details</th>\n    </tr>\n    <tr>\n      <th>Attribute</th>\n      <th></th>\n    </tr>\n  </thead>'
	replace_with = '<thead>\n <tr style="text-align: right;">\n <th>Attribute</th>\n <th>Details</th>\n </tr>\n </thead>'
	mars_table_html = mars_table_html.replace(to_replace, replace_with)
	# Display Downloaded Image
	#     from IPython.display import HTML
	#     display(HTML(filename='table.html'))
	# save html to variable
	# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– #
	# ### Retrieve images of Mars' four hemispheres from [the Astrogeology Science Center]
	# (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)<br>
	# #### The Hemispheres are:
	#     - Cerberus
	#     - Schiaparelli
	#     - Syrtis Major
	#     - Valles Marineris
	# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– #
	#     - Cerberus
	# Start @ USGS homepage
	# browser = Browser("chrome", **executable_path, headless=False)
	asgeo_home = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(asgeo_home)
	# On automate clicking on 'Cereberus' image;
	xpath = '//*[@id="product-section"]/div[2]/div[1]/a/img'
	results = browser.find_by_xpath(xpath)
	img = results[0]
	img.click()
	# goal: Parse html to pinpoint image url;
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	# go back to homepage (after copying html) & print html body;
	browser.back()
	cerberus_href = soup.find('a', text='Original').get('href')
	cerberus_sample_href = soup.find('a', text='Sample').get('href')
	# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– #
	#     - Schiaparelli
	# On automate clicking on 'Schiaparelli' image;
	xpath = '//*[@id="product-section"]/div[2]/div[2]/a/img'
	results = browser.find_by_xpath(xpath)
	img = results[0]
	img.click()
	# goal: Parse Schiaparelli html to pinpoint image url;
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	# go back to homepage (after copying html) & print html body;
	browser.back()
	Schiaparelli_href = soup.find('a', text='Original').get('href')
	Schiaparelli_sample_href = soup.find('a', text='Sample').get('href')
	# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– #
	#     - Syrtis Major
	# On automate clicking on 'Syrtis Major' image;
	xpath = '//*[@id="product-section"]/div[2]/div[3]/a/img'
	results = browser.find_by_xpath(xpath)
	img = results[0]
	img.click()
	# goal: Parse Syrtis Major html to pinpoint image url;
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	# go back to homepage (after copying html) & print html body;
	browser.back()
	Syrtis_Major_href = soup.find('a', text='Original').get('href')
	Syrtis_Major_sample_href = soup.find('a', text='Sample').get('href')
	# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– #
	#     - Valles Marineris
	# On automate clicking on 'Valles Marineris' image;
	xpath = '//*[@id="product-section"]/div[2]/div[4]/a/img'
	results = browser.find_by_xpath(xpath)
	img = results[0]
	img.click()
	# goal: Parse Valles Marineris html to pinpoint image url;
	html = browser.html
	soup = BeautifulSoup(html, 'html.parser')
	# print html body;
	# print(soup.body.prettify())
	Valles_Marineris_href = soup.find('a', text='Original').get('href')
	Valles_Marineris_sample_href = soup.find('a', text='Sample').get('href')


	all_mars_urls = [
	{"title": "Valles Marineris Hemisphere", 
	"img_url": Valles_Marineris_href,
	'sample_url': Valles_Marineris_sample_href},
	{"title": "Cerberus Hemisphere", 
	"img_url": cerberus_href,
	'sample_url': cerberus_sample_href},
	{"title": "Schiaparelli Hemisphere", 
	"img_url": Schiaparelli_href,
	'sample_url': Schiaparelli_sample_href},
	{"title": "Syrtis Major Hemisphere", 
	"img_url": Syrtis_Major_href,
	'sample_url': Syrtis_Major_sample_href},
	{"article_title": article_title, 
	"article_paragraph": article_paragraph},
	{"featured_img_url": featured_img_url},
	{"mars_weather": mars_weather},
	{"mars_table_html": mars_table_html}
	]

	browser.quit()

	return all_mars_urls


#
#
# Step 2 - MongoDB and Flask Application
# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was
# scraped from the URLs above.
#
# Start by converting your Jupyter notebook into a Python script called scrape_mars.py with a function called
# scrape that will execute all of your scraping code from above and return one Python dictionary containing
# all of the scraped data.
#
# Next, create a route called /scrape that will import your scrape_mars.py script and call your scrape function.
#
# Store the return value in Mongo as a Python dictionary.
# Create a root route / that will query your Mongo database and pass the mars data into an HTML template to
# display the data.
#
# Create a template HTML file called index.html that will take the mars data dictionary and display all of
# the data in the appropriate HTML elements. Use the following as a guide for what the final product should look
# like, but feel free to create your own design.

# Step 3 - Submission
# To submit your work to BootCampSpot, create a new GitHub repository and upload the following:
#
# The Jupyter Notebook containing the scraping code used.
# Screenshots of your final application.
#

# Use Pymongo for CRUD: Create, Read, Update, Delete applications for your database.