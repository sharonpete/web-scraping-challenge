import requests
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    # Set up splinter
    executable_path = {'executable_path':ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def init_mongodb():
    # Initialize PyMongo to work with MongoDBs
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    return client

def scrape():
    print("Now scraping -----------")
    # Create dictionary object to return the scraped data
    dict_mars = {}

    # NASA Mars News ....
    print("NASA Mars News")
    # Use the splinter browser... 
    nasa_url = "https://redplanetscience.com/"
    browser = init_browser()
    browser.visit(nasa_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('div', class_='list_text')

    # client = init_mongodb()

    # db = client.nasa_db
    # collection = db.items

    nasa_news_articles = []
    # Loop through results 
    for result in results:
        try:
            title = result.find('div', class_='content_title').text
            blurb = result.find('div', class_='article_teaser_body').text
          
            if (title and blurb):
                post = {
                    'title': title,
                    'blurb': blurb}
                
                nasa_news_articles.append(post)
       
        except Exception as e:
            print(e)
    dict_mars['nasa_news_articles'] = nasa_news_articles
 
    # JPL Mars Space Images - Featured Image
    #print("JPL Mars Space Images - Featured Image")
    jpl_url = "https://spaceimages-mars.com/"

    browser.visit(jpl_url)

    html = browser.html
    jpl_soup = BeautifulSoup(html, 'html.parser')
    
    jpl_results = jpl_soup.find_all('img', class_='headerimage fade-in')

    featured_image_url = f"{jpl_url}{jpl_results[0]['src']}"
    dict_mars['featured_image_url'] = featured_image_url

    # try:
    #     #post = {'featured_image_url':featured_image_url}
    #     #collection.insert_one(post)
    #     dict_mars['featured_image_url'] = featured_image_url

    # except Exception as e:
    #     print(e) 
    
    browser.quit()

    # Mars Facts
    #print("Mars Facts from galaxyfacts-mars.com")
    mars_facts_url = 'https://galaxyfacts-mars.com/'

    tables = pd.read_html(mars_facts_url)
    
    mars_earth_table_df = tables[0]
    mars_profile_table_df = tables[1]
    
    me_list = mars_earth_table_df.loc[0]
    mars_earth_table_df.columns = me_list
   
    mp_list =["Mars Attribute", "Measurement"]
    mars_profile_table_df.columns = mp_list
    
    dict_mars['mars_earth_table_html'] = mars_earth_table_df.to_html()
    dict_mars['mars_profile_table_html'] = mars_profile_table_df.to_html()


    # Mars Hemispheres  - high resolutions images for each of Mars' hemispheres
    USGS_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    base_USGS_url = "https://astrogeology.usgs.gov"
    browser.visit(USGS_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('div', class_='item')
 
    hemisphere_image_urls = []

    for result in results:
        title = result.find('h3').text
        href = result.find('a')['href']
        img_url = f'{base_USGS_url}{href}'
        print(img_url)
        browser.visit(img_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        original_img = soup.find('div', class_='downloads')
        img_url = original_img.find('a')['href']
        hemi = {'title':title, 'img_url': img_url}
        hemisphere_image_urls.append(hemi)

   
    dict_mars['hemisphere_image_urls'] = hemisphere_image_urls
    brower.quit()

    client = init_mongodb()
    db = client.nasa_db
    collection = db.items
    
    try:  
        collection.insert_one(dict_mars)
        
    except Exception as e:
        print(e)

    print(f'in scrape_mars.py, this is the return: {dict_mars}')
    return dict_mars
# Let's do the thing
print('scrape_mars.py now running.... ')

scrape()



