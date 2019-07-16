from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    listings = {}

    # Scrape NASA Mars news page into Soup
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    news = soup.find("div", class_ = "list_text")

    news_title = news.find('div', class_ ='content_title').get_text()
    news_teaser = news.find('div', class_ ='article_teaser_body').get_text()  

    
    # Scrape NASA Mars Image into Soup
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    image = soup.find("div", class_ = "carousel_items")

    featured_image_url = url[:24]+image.find('article')['style'][23:-3]

    
    # Scrape NASA Mars twitter page into Soup
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    # Select top Mars Weather Report tweet
    twit0 = soup.find("div", class_ = "tweet", attrs={"data-screen-name": "MarsWxReport"})

    # Retrive Weather Report Text
    twit = twit0.find("p", class_ = "tweet-text").get_text()

    # Clean string
    mars_weather = twit.replace("\n"," ").split("pic.twitter.com")[0]


    

    # Scrape Mars Facts into Soup using Python Pandas
    url = "https://space-facts.com/mars/"
    mars_facts = pd.read_html(url)
    mars_facts_df = mars_facts[1]
    mars_facts_df.columns = ['Description','Value']
    mars_facts_htm = mars_facts_df.to_html(index = False, justify = 'left', classes = "table-bordered", table_id = 'mars_facts_tbl')\
                    .replace("\n","")\
                    .replace("> ",">").replace("> ",">").replace("> ",">")\
                    .replace("> ",">").replace("> ",">").replace("> ",">")

    
    # Scrape Mars' hemisphere images from the USGS Astrogeology page into Soup
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "lxml")

    # Select all Mars Hemisphere items
    hemispheres = soup.find_all("div", class_ = "item")
    
    title = []
    hemis_page = []
    
    # Retrieve each hemisphere title and page
    for item in range(len(hemispheres)):
        title.append(hemispheres[item].find("h3").get_text())
        hemis_page.append(hemispheres[item].find("a", class_ = "itemLink").get('href'))
        
    hemisphere_image_urls = []
    base_url = 'https://astrogeology.usgs.gov'
    
    # Retrieve each hemisphere full resolution image url string
    # Append hemisphere dictionary to list
    for img in range(len(hemis_page)):
            url = base_url + hemis_page[img]
            browser.visit(url)
            html = browser.html
            soup = bs(html, "lxml")
            hemisphere_image_urls.append({'title': title[img],'img_url': soup.find("a", string = "Sample").get('href')})

    # Store data in a dictionary
    mars_database = {
        "news_title": news_title,
        "news_teaser": news_teaser,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts_htm": mars_facts_htm,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_database

if __name__ == "__main__":
    mars_database = scrape()
    print(mars_database)