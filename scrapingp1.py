#PART 1: EXTRACTING EVERY PASTOR HOME PAGE LINK
#only requirement = at least contributed 2 sermons

#input: none
#output: pastor_links.csv in temp folder (every pastor's home page given they've contributed at least 2 sermons)

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import csv
import os

# URL for all pastors that have contributed to Sermon Central (sorted newest first)
base_url = "https://www.sermoncentral.com"
all_contribs = f"{base_url}/Contributors/Search/?sortBy=SermonShared&keyword=&rewrittenurltype=&searchResultSort=SermonShared&denominationFreeText="

def get_soup(url):
    print("Fetching URL:", url)
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Failed to fetch or parse {url}: {e}")
        return None

#from all contributors home page, getting all pastor links to their home pages
def scrape_pastors_links(base_url, all_contribs):
    all_pastor_links = set()  

    # loop through pages 1 to 370 (after page 370 only 1 sermon contributed)
    for page_num in range(1, 370):  
        page_url = f"{all_contribs}&page={page_num}"
        soup_page = get_soup(page_url)
        if soup_page is not None:
            links = soup_page.find_all('a', href=lambda href: href and re.search("/contributors", href) and re.search("profile", href))
            pastor_links = set([link['href'] for link in links])
            all_pastor_links.update(pastor_links)
        else:
            print(f"Skipping page {page_num} due to fetch error")

    unique_pastor_links = list(all_pastor_links) 
    return unique_pastor_links

unique_pastor_links = scrape_pastors_links(base_url, all_contribs)

print("Total Number of Pastor Links Found:", len(unique_pastor_links))


csv_filename = 'pastor_links.csv'

desktop_path = '/Users/liadougherty/Desktop/temp'
os.makedirs(desktop_path, exist_ok=True)  
csv_filename = os.path.join(desktop_path, 'pastor_links.csv')

with open(csv_filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Link']) 

    for link in unique_pastor_links[:-1]:
        url = f"{base_url}{link}"
        print(url)
        csvwriter.writerow([url])  

print(f"All links except the last one have been saved to {csv_filename}")
