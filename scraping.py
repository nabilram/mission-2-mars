# Import Dependencies
# Splinter, BeautifulSoup, Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Setup Splinter Browser
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

#### 1 - SCRAPE MARS NEWS ARTICLE
def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Connvert HTML in browser to a soup object and parse 
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Adding Try and Except for Error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag (for article title) and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #news_title

        # Use the parent element to find the paragraph text - article teaser
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        #news_p
    except AttributeError:
        return None, None
    
    return news_title, news_p

##### 2 - SCRAPE FEATURED IMAGES
def featured_image(browser):
    # Visit the space image website
    url2 = 'https://spaceimages-mars.com'
    browser.visit(url2)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try and except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #img_url_rel

        # Use the base URL to create an absolute URL becuse SRC link is only partial
        img_url = f'https://spaceimages-mars.com/{img_url_rel}'
        #img_url
    except AttributeError:
        return None

    return img_url

#### 3 - SCRAPE MARS FACTS
# Use pandas to visit site, pull table
# Convert to DF and reconvert back to HTML table

def mars_facts():
    # Add try except for error handling -- Base Exeption since errors
    # other than Attribute errors may occur (since were scraping a table with pandas)
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    # Add column names and set 1st column (desc) as index
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    #df

#convert pulled df into html + bootstrap
    return df.to_html()

browser.quit()