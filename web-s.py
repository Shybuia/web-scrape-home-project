import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import scraping
import time
import pandas as pd

script_start_time = time.strftime("%d_%m_%Y-%H%M%S")

def find_and_scrape_sublinks(url):
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    urls = []
    url_end_removed = re.sub('\?modul=bazar&od=\d{1,3}', '', url)
    search_text = url_end_removed.replace('/','\/').replace('.','\.') + '\/'      
    for link in soup.find_all('a'):
        text = link.get('href')                     
        found_link = re.search(search_text, str(text))
        if found_link:        
            urls.append(text)     
    for line in dict.fromkeys(urls):
        print(line)    
        scraping.scrape_page(line, script_start_time)                    

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
    page_range = get_page_range(url)    
    for i in range (0, int(max(page_range)) + 1):            
        completeURL = url.rstrip('/') + '?modul=bazar&od=' + str(i)                
        find_and_scrape_sublinks(completeURL)

# main('https://www.mtbiker.sk/bazar/bicykle/horske-bicykle/pevne-a-hardtail/')
main('https://www.mtbiker.sk/bazar/bicykle/horske-bicykle/celoodpruzene/')

file_name = script_start_time + "_export.csv"
file_name_output = script_start_time + "_export_without_dupes.csv"
df = pd.read_csv(file_name, sep=",", engine='python')
df.drop_duplicates(subset=None, inplace=True)
df.to_csv(file_name_output, index=False)