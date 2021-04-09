import requests
import pymongo
from splinter import Browser
from b24 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    # Set up splinter
    executable_path = {'executable_path':ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    # NASA Mars News ....
    # Use the splinter browser... 
    nasa_url = "https://redplanetscience.com/"

    browser.visit(nasa_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('div', class_='list_text')

    # Initialize PyMongo to work with MongoDBs
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    db = client.nasa_db
    collection = db.items

    # Loop through results and populate Mongo nasa_db
    for result in results:
        try:
            title = result.find('div', class_='content_title').text
            blurb = result.find('div', class_='article_teaser_body').text
            
    #         print('**************')
    #         print(f'Title: {title}')
    #         print(f'Blurb: {blurb}')
            
            # gather up the items for mongo db
            if (title and blurb):
            post = {
                'title': title,
                'blurb': blurb,
                }

            collection.insert_one(post)
        except Exception as e:
            print(e)
    
    # JPL Mars Space Images - Featured Image

    jpl_url = "https://spaceimages-mars.com/"

    browser.visit(jpl_url)

    html = browser.html
    jpl_soup = BeautifulSoup(html, 'html.parser')
    #jpl_soup

    #jpl_results = jpl_soup.find_all('div', class_='floating_text_area')
    jpl_results = jpl_soup.find_all('img', class_='headerimage fade-in')

    featured_image_url = f"{jpl_url}{jpl_results[0]['src']}"
    #featured_image_url

    # Mars Facts
    mars_facts_url = 'https://galaxyfacts-mars.com/'

    tables = pd.read_html(mars_facts_url)
    #tables
    mars_earth_table_df = tables[0]
    #mars_earth_table_df

    mars_profile_table_df = tables[1]
    me_list = mars_earth_table_df.loc[0]
    mars_earth_table_df.columns = me_list

    #mars_earth_table_df

    print(mars_earth_table_df.to_html())

    mp_list =["Mars Attribute", "Measurement"]
    mars_profile_table_df.columns = mp_list

    print(mars_profile_table_df.to_html())

    # Mars Hemispheres  - high resolutions images for each of Mars' hemispheres
    hemi_base_url = "https://marshemispheres.com/images/"

    # Valles Marineris
    valles_marineris_url = f'{hemi_base_url}valles_marineris_enhanced.tif'

    # Cerberus
    cerberus_url = f'{hemi_base_url}cerberus_enhanced.tif'

    # Schiaparelli 
    schiaparelli_url = f'{hemi_base_url}schiaparelli_enhanced.tif'

    # Syrtis Major
    syrtis_major_url = f'{hemi_base_url}syrtis_major_enhanced.tif'

    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": valles_marineris_url},
        {"title": "Cerberus Hemisphere", "img_url": cerberus_url},
        {"title": "Schiaparelli Hemisphere", "img_url": schiaparelli_url},
        {"title": "Syrtis Major Hemisphere", "img_url": syrtis_major_url},
    ]

    hemisphere_image_urls



    