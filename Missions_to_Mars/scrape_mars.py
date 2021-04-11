from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd



def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    mars_data = {}

    # NASA Mars News
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html

    soup = bs(html, 'html.parser')

    # news_title = soup.find('div', class_='content_title').text
    # news_p = soup.find('div', class_='article_teaser_body').text

    mars_data['news_title'] = soup.find('div', class_='content_title').text
    mars_data['news_p'] = soup.find('div', class_='article_teaser_body').text

    # JPL Mars Space Images
    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)
    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
        
    featured_image_url = soup.find('img', class_='headerimage fade-in')

    #featured_image_url = image_url + featured_image_url['src']

    mars_data['featured_image_url'] = image_url + featured_image_url['src']

    ## Mars Facts
    url ='https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    df = tables[0]
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    df.set_index('Mars - Earth Comparison',inplace=True)

    html_table = df.to_html()

    mars_data['table'] = html_table

    ## Mars Hemispheres
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    hemisphere_image_urls = []
    hem_url = browser.find_element_by_css_selector('a', class_='itemLink product-item')

    for item in range(len(hem_url)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3").click()
        mars_data["hem_title"] = browser.find_by_css("h2.title").text

        sample_element = browser.find_link_by_text("Sample").first
        mars_data["hem_img_url"] = sample_element["href"]
        
        
        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate Backwards
        browser.back()

    # Quit the browser
    browser.quit()

    return mars_data

    

