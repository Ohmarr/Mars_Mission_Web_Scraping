<h1 align = 'center'> Mission to Mars </h1>

<h3 align = 'center'> A web-scraping application, which aggregates information from various online resources and displays the results on a landing page </h3>

![mission_to_mars](Images/jpl_fullsize_image.jpg)

This application utilized Jupyter Notebook, BeautifulSoup, Pandas, Splinter, PyMongo, Flask Web Templating, & requests.
CRUD


<h2 align='center>Scraping</h2>

Scraping was developed in Jupyter Notebook File `mission_to_mars.ipynb`, which was later converted into a function called `scrape` within a new file called `scrape_mars.py`

Information was gathered from: 
 - [NASA Mars News Site](https://mars.nasa.gov/news/), Scraped: Latest News Title & Paragraph Text,
 - [Jet Propulsion Laboratories (JPL)](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars), Scraped: Featured Image, 
 - [Mars Weather - Twitter Account](https://twitter.com/marswxreport?lang=en), Scraped: Latest Weather Tweet,
 - [Space Facts Website](http://space-facts.com/mars/), Scraped: Tables Containing Planet Attributes & Information, 
 - [United States Geological Survery (USGS)](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars), Scraped: Hi-Res Images of each of Mars' Hemispheres, 


<hr>

<h2 align='center> MongoDB and Flask Application</h2>

The file `app.py` contains the main application, which populates an HTML page from the contents of a database.  

The aggregated information from above *Scraping* is stored in a MongoDB database, and is updated with the latest information every time the application is run (CRUD).  

Flask web-templating was used to create a few routes, including a new landing page, which displays the gathered information from the database. 

The routes are:
 - `/` - The Landing Page (Home), which queries the database, & populates the contents,
 - `/scrape` - Runs `scrape` function from `scrape_mars.py`, and updates database,
