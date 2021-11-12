import requests
from bs4 import BeautifulSoup
URL = "https://www.mtbiker.sk/bazar/bicykle/horske-bicykle/celoodpruzene/484534/lapierre-spicy-2019.html"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="bazaar-item-484534")
# print(results.prettify())
job_elements = results.find_all("h1", class_="mb-0")
for job_element in job_elements:
    print(job_element.text.strip(), end="\n"*2)