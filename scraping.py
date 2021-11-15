import re
from bs4 import BeautifulSoup

def scrape_page(URL, session):    
    find_id = re.search('\/(\d{1,9})\/', URL)
    if find_id:
        found_id = find_id.group(1)
    page = session.get(URL)    
    soup = BeautifulSoup(page.content, "html.parser")    
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
    find_categories = re.search('\/bicykle\/(?<=\/)(.*?)\/(.*?)(?=\/)', str(URL))
    if find_categories:
        category = find_categories.group(1)
        sub_category = find_categories.group(2)
    else:
        category = 'none'
        sub_category = 'none'                 
    return found_id, title, cost, model_year, URL, category, sub_category

# scrape_page('https://www.mtbiker.sk/bazar/bicykle/horske-bicykle/pevne-a-hardtail/479013/force-tron-l-.html')

