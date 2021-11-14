# Import Dependencies
# Splinter, BeautifulSoup, Pandas, DateTime
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


# Setup Splinter Browser

def scrape_all():
    # Initiate headless(?) driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

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
        #slide_elem.find('div', class_='content_title')

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

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL becuse SRC scraped URL is only partial
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

#### 3 - SCRAPE MARS FACTS
# Use pandas to visit site, pull table
# Convert to DF and reconvert back to HTML table

def mars_facts():
    # Add try except for error handling -- Base Exeption since errors
    # other than Attribut Errors may occur (since were scraping a table with pandas)
    try:
        #read_html to convert table, index it to fond the first one
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Add column names and set 1st column (desc) as index
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    

    #convert pulled df into html + bootstrap (striped table)
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":
    # If this is being ran as a script, then print scraped data
    print(scrape_all())