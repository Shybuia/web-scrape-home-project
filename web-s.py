import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import scraping
import time
import pandas as pd

def find_and_scrape_sublinks(url):
    session = requests.Session()
    reqs = session.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    urls = []
    scraped_pages = []        
    url_end_removed = re.sub('\?modul=bazar&od=\d{1,3}', '', url)
    search_text = url_end_removed.replace('/','\/').replace('.','\.') + '\/'      
    for link in soup.find_all('a'):
        text = link.get('href')                     
        found_link = re.search(search_text, str(text))
        if found_link:        
            urls.append(text)     
    for sub_link in dict.fromkeys(urls):
        print(sub_link)    
        scraped_pages.append(scraping.scrape_page(sub_link, session))
    return scraped_pages

def get_page_range(url):
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')    
    page_indexes = []
    search_text = url.replace('/','\/').replace('.','\.').rstrip('\/')
    search_text = search_text + '\?modul=bazar&od='    
    for link in soup.find_all('a'):
        text = link.get('href')                
        found_link = re.search(search_text, str(text))        
        if found_link:        
            processed_text = re.sub(search_text, '',text)
            page_indexes.append(processed_text)                
    return list(dict.fromkeys(page_indexes))

def main(url):    
    scraped_pages = []
    script_start_time = time.strftime("%d_%m_%Y-%H%M%S")
    file_name = script_start_time + "_export.csv"
    page_range = get_page_range(url)    
    for i in range (0, int(max(page_range)) + 1):                
        completeURL = url.rstrip('/') + '?modul=bazar&od=' + str(i)             
        scraped_pages += find_and_scrape_sublinks(completeURL)    
    dataframe = pd.DataFrame(scraped_pages, columns=['id','title','model_year','cost','url','category','sub_category'])
    dataframe.drop_duplicates(subset=None, inplace=(True))
    dataframe.to_csv(file_name, index=False)

main('https://www.mtbiker.sk/bazar/bicykle/horske-bicykle/pevne-a-hardtail/')
# main('https://www.mtbiker.sk/bazar/bicykle/horske-bicykle/celoodpruzene/')
# main('https://www.mtbiker.sk/bazar/bicykle/cestne-bicykle')