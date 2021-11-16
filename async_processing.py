import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def get_sublinks(url, session):
    try:
        async with session.get(url=url) as response:
            resp = await response.read()
            print("Successfully got url {} with resp of length {}.".format(url, len(resp)))            
            soup = BeautifulSoup(resp, 'html.parser')   
            urls = []
            pages_urls = []        
            url_end_removed = re.sub('\?modul=bazar&od=\d{1,3}', '', url)
            search_text = url_end_removed.replace('/','\/').replace('.','\.') + '\/'      
            for link in soup.find_all('a'):
                text = link.get('href')                     
                found_link = re.search(search_text, str(text))
                if found_link:        
                    urls.append(text)     
            for sub_link in dict.fromkeys(urls):
                print(sub_link)
                pages_urls.append(sub_link)
            return pages_urls
                        
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))


async def sublinks_async(urls):
    async with aiohttp.ClientSession() as session:        
        list_to_return = []
        ret = await asyncio.gather(*[get_sublinks(url, session) for url in urls])
        for link in ret:
            print(link)
        for i in range(len(ret)) : 
            for j in range(len(ret[i])) :                 
                list_to_return.append(ret[i][j])
        return list_to_return    

async def async_scraping(url, session):
    try:
        async with session.get(url=url) as response:
            resp = await response.read()            
            print("Successfully got url {} with resp of length {}.".format(url, len(resp)))                     
            soup = BeautifulSoup(resp, 'html.parser') 
            find_id = re.search('\/(\d{1,9})\/', url)
            if find_id:
                found_id = find_id.group(1)  
            results = soup.find(id="bazaar-item-" + found_id)
            title = results.find("h1", class_="mb-0").text.strip()
            cost = results.find("span", class_="badge badge-pill badge-dark align-text-bottom").text.strip().replace('.','')        
            sub_results = soup.find(id="bazaar-detail-tabs")
            details = sub_results.find_all("p", class_="text-line-height-lg")
            for detail in details:    
                find_model_year = re.search('Modelový rok:</strong> (\d\d\d\d)', str(detail))
                if find_model_year:        
                    model_year = find_model_year.group(1)    
                else:
                    model_year='not defined'        
            find_categories = re.search('\/bicykle\/(?<=\/)(.*?)\/(.*?)(?=\/)', str(url))
            if find_categories:
                category = find_categories.group(1)
                sub_category = find_categories.group(2)
            else:
                category = 'none'
                sub_category = 'none'      
                        
            return found_id, title, cost, model_year, url, category, sub_category

                        
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))

async def scraping_async_main(urls):
    async with aiohttp.ClientSession() as session:
        scraped_pages_to_return = []        
        ret = await asyncio.gather(*[async_scraping(url, session) for url in urls])
        return ret

# parsed_pages_urls = asyncio.run(sublinks_async(pages_urls))
# scraped_pages = asyncio.run(scraping_async_main(parsed_pages_urls))