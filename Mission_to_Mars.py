#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importing dependencies and libraries
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


# In[2]:


#Defining an executable path
def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


# In[3]:


#Showing DF for Mars facts

# Defining URL
url = "https://space-facts.com/mars/"

# Parsing URL to DF
mars_facts_df = pd.read_html(url)[1]

# Retrieving columns of interest showing results setting index
mars_facts_df.columns = ['Description','Value']
mars_facts_df.set_index('Description', inplace=True) 
mars_facts_df


# In[4]:


#Defining a Scrape function 

def scrape():
    browser = init_browser()
    listings = {}

    # Scraping NASA Mars news page into Soup
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    news = soup.find("div", class_ = "list_text")
    news_title = news.find('div', class_ ='content_title').get_text()
    news_teaser = news.find('div', class_ ='article_teaser_body').get_text()  
    
    
    # Scraping NASA Mars twitter page into Soup
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    
    # Select top Mars Weather Report tweet
    twit_class = soup.find("div", class_ = "tweet", attrs={"data-screen-name": "MarsWxReport"})

    # Retrive Weather Report Text
    twit_text = twit_class.find("p", class_ = "tweet-text").get_text()

    # Clean string
    mars_current_weather = twit_text.replace("\n"," ").split("pic.twitter.com")[0]

    
    # Scraping NASA Mars Image into Soup
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    image = soup.find("div", class_ = "carousel_items")
    featured_image_url = url[:24]+image.find('article')['style'][23:-3]    
  
    
    # Scraping Mars Facts into Soup using Python Pandas
    url = "https://space-facts.com/mars/"
    mars_facts = pd.read_html(url)
    mars_facts_df = mars_facts[1]
    mars_facts_df.columns = ['Description','Value']
    mars_facts_htm = mars_facts_df.to_html(index = False, justify = 'left', table_id = 'mars_facts_tbl')                    .replace("\n","")                    .replace("> ",">").replace("> ",">").replace("> ",">")                    .replace("> ",">").replace("> ",">").replace("> ",">")

    
    # Scraping Mars' hemisphere images from the USGS Astrogeology page into Soup
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "lxml")

    # Select all Mars Hemisphere items
    hemispheres = soup.find_all("div", class_ = "item")
    
    title = []
    hemisphere_page = []
    
    # Retrieve each hemisphere title and page
    for item in range(len(hemispheres)):
        title.append(hemispheres[item].find("h3").get_text())
        hemisphere_page.append(hemispheres[item].find("a", class_ = "itemLink").get('href'))
        
    hemisphere_image_urls = []
    base_url = 'https://astrogeology.usgs.gov'
    
    # Retrieve each hemisphere image url string and append hemisphere dictionary to list
    for img in range(len(hemisphere_page)):
            url = base_url + hemisphere_page[img]
            browser.visit(url)
            html = browser.html
            soup = bs(html, "lxml")
            hemisphere_image_urls.append({'title': title[img],'img_url': soup.find("a", string = "Sample").get('href')})

 
   # Storing data in a dictionary
 
    mars_database = {
        "news_title": news_title,
        "news_teaser": news_teaser,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_current_weather,
        "mars_facts_htm": mars_facts_htm,
        "hemisphere_image_urls": hemisphere_image_urls
    }
    
    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_database


# In[5]:


scrape()


# In[ ]:




