#PART 3: Finding Pastor Info (pastor name, church name, address, num sermons, denomination, link) from the filtered links homepage

#input: filtered_pastor_links.csv in temp folder
#output: pastor_info in temp folder

import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_soup(url):
    print("Fetching URL:", url)
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Failed to fetch or parse {url}: {e}")
        return None

#getting pastor name
def get_pastor_name(soup):
    h4_tag = soup.find('h4', class_='title')
    if h4_tag:
        pastor_name = h4_tag.text.strip()
        # removing "Pastor/Author" prefix
        if pastor_name.startswith("Pastor/Author"):
            pastor_name = pastor_name[len("Pastor/Author"):].strip()
        # remove ": " from the title
        pastor_name = pastor_name.split(": ")[-1]
        return pastor_name

#getting church name
def get_church(soup):
    strong_tag = soup.find('strong', string='Church Name: ')
    if strong_tag:
        church = strong_tag.find_next_sibling(string=True).strip()
        return church
    return "None"

#getting number of sermons
def get_num_sermons(soup):
    strong_tag = soup.find('strong', string='Sermons Contributed: ')
    if strong_tag:
        next_element = strong_tag.find_next_sibling()
        if next_element and next_element.name == 'a':
            sermon_count = next_element.text.strip()
            return int(sermon_count)
    return 0

#getting denomination
def get_denomination(soup):
    strong_tag = soup.find('strong', string='Denomination: ')
    if strong_tag:
        next_sibling = strong_tag.find_next_sibling()
        if next_sibling and next_sibling.name == 'a':
            denomination = next_sibling.text.strip()
            return denomination
    return "None"

#getting address
def get_address(soup):
    legend_tag = soup.find('legend', string=re.compile(r"'s church", re.IGNORECASE))
    if legend_tag:
        p_tag = legend_tag.find_next_sibling('p')
        if p_tag:
            address_info = p_tag.get_text(separator='\n').strip()
            address_lines = address_info.split('\n')[1:-1]  # Exclude first and last lines
            cleaned_address = '\n'.join(address_lines).strip()
            if cleaned_address:
                return cleaned_address
    return "None"



def main():

    desktop_path = '/Users/liadougherty/Desktop/temp'
    os.makedirs(desktop_path, exist_ok=True)  

    input_file_path = os.path.join(desktop_path, "filtered_pastor_links.csv")
    output_file_path = os.path.join(desktop_path, "pastor_info.csv")

    try:
        df = pd.read_csv(input_file_path)
        print("File successfully loaded into DataFrame.")
    except FileNotFoundError:
        print("File path is invalid or the file does not exist.")
        return

    pastor_info = []

    for index, row in df.iterrows():
        url = row['Link']
        soup = get_soup(url)
        if soup:
            pastor_name = get_pastor_name(soup)
            church_name = get_church(soup)
            address = get_address(soup)
            num_sermons = get_num_sermons(soup)
            denomination = get_denomination(soup)
            pastor_info.append({
                'Pastor Name': pastor_name,
                'Church Name': church_name,
                'Address': address,
                'Number of Sermons': num_sermons,
                'Denomination': denomination,
                'Filtered Link': url 
            })

    pastor_info_df = pd.DataFrame(pastor_info)

    pastor_info_df.to_csv(output_file_path, index=False)
    print("Pastor information saved to:", output_file_path)

if __name__ == "__main__":
    main()
