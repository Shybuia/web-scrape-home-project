import requests
import re
from bs4 import BeautifulSoup
import scraping
import time
import pandas as pd

def find_sublinks(url):
    urls = []
    pages_urls = []        
    session = requests.Session()
    reqs = session.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    url_end_removed = re.sub('\?modul=bazar&od=\d{1,3}', '', url)
    search_text = url_end_removed.replace('/','\/').replace('.','\.') + '\/'      
    for link in soup.find_all('a'):
        text = link.get('href')                     
        found_link = re.search(search_text, str(text))
        if found_link:        
            urls.append(text)     
    for sub_link in dict.fromkeys(urls):
        pages_urls.append(sub_link)
    return pages_urls
            
def get_page_range(url):
    page_indexes = []
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')    
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
    parsed_pages_urls = []    
    page_range = get_page_range(url)    
    for i in range (0, int(max(page_range)) +1 ):                
        completeURL = url.rstrip('/') + '?modul=bazar&od=' + str(i)                     
        print(completeURL)        
        parsed_pages_urls = parsed_pages_urls + find_sublinks(completeURL)            
    parsed_pages_urls = dict.fromkeys(parsed_pages_urls)
    counter = 0
    for url in parsed_pages_urls:
        counter += 1
        print(counter)
        scraped_pages.append(scraping.scrape_page(url))        
    print(max(page_range))     
    return scraped_pages       

scraped_pages = []
scraped_pages = main('https://www.mtbiker.sk/bazar/bicykle/horske-bicykle/pevne-a-hardtail/')
scraped_pages += main('https://www.mtbiker.sk/bazar/bicykle/horske-bicykle/celoodpruzene/')
scraped_pages += main('https://www.mtbiker.sk/bazar/bicykle/cestne-bicykle')
script_start_time = time.strftime("%d_%m_%Y-%H%M%S")
file_name = script_start_time + "_export.csv"
dataframe = pd.DataFrame(scraped_pages, columns=['id','title','model_year','cost','url','category','sub_category'])
dataframe.drop_duplicates(subset=None, inplace=(True))
dataframe.to_csv(file_name, index=False)