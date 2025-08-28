#PART 7 (2/2)
#DUPLICATES PROBLEM

#creating sermon text files for only the duplicate named sermons
#since meteodology is a bit different in naming the files (don't want to just extract titles since they have the same ones)


#input: pastor_info_wsermons_duplicates.csv in temp folder
#output: sermon files in temp folder

import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import os

#normalizing pastor name to help extract title
def normalize_pastor_name(name):
    name = name.lower()
    name = re.sub(r'[^\w\s]', '', name)
    return name

#getting the sermon title from URL
#for duplicates, using full URL to avoid more duplicate titles
def get_sermon_title(url, name):
   return url

#getting date from subtitle
def extract_date_from_subtitle(subtitle_text):
    match = re.search(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4}', subtitle_text)
    return match.group(0) if match else "Date not found"

#getting date contributed
def get_date_contributed(soup):
    subtitle_element = soup.find('h2', class_='subtitle')
    if subtitle_element:
        subtitle_text = subtitle_element.get_text().strip()
        return extract_date_from_subtitle(subtitle_text)
    else:
        return "Date of contribution information not found"

#getting total number of sermon pages
def get_total_sermon_pages(soup):
    page_tags = soup.find_all('a', class_='page')
    return max([int(tag.text) for tag in page_tags]) if page_tags else 1

#getting the sermon text
def get_sermon_text(url, total_sermon_pages_sermon):
    sermon_text = ""
    for page in range(1, total_sermon_pages_sermon + 1):
        page_url = f"{url}?page={page}"
        response = requests.get(page_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            sermon_div = soup.find('div', id='TheSermonText')
            if sermon_div:
                sermon_text += sermon_div.get_text(separator='\n', strip=True) + "\n"
    return sermon_text

def main():
    desktop_path = '/Users/liadougherty/Desktop/temp'
    os.makedirs(desktop_path, exist_ok=True)  

    input_file_path = os.path.join(desktop_path, 'pastor_info_wsermons_duplicates.csv')
    df = pd.read_csv(input_file_path)

    for idx, row in df.iterrows():
        pastor_name = row['Pastor Name']
        church_name = row['Church Name']
        address = row['Address']
        number_of_sermons = row['Number of Sermons']
        denomination = row['Denomination']
        sermon_links = row['Sermon Links'].split(', ')

        #normalized pastor name
        normalized_pastor_name = normalize_pastor_name(pastor_name)

        #processing each sermon link for the current pastor
        for i, link in enumerate(sermon_links):
            title = get_sermon_title(link, normalized_pastor_name)
            response = requests.get(link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                date_contributed = get_date_contributed(soup)
                total_sermon_pages_sermon = get_total_sermon_pages(soup)
                sermon_text = get_sermon_text(link, total_sermon_pages_sermon)

                #creating the file name
                file_name = os.path.join(desktop_path, f"sermon_files/{title}_{pastor_name.replace(' ', '_')}.txt")

                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(f"Pastor Name: {pastor_name}\n")
                    f.write(f"Church Name: {church_name}\n")
                    f.write(f"Address: {address}\n")
                    f.write(f"Number of Sermons: {number_of_sermons}\n")
                    f.write(f"Denomination: {denomination}\n")
                    f.write(f"Title: {title}\n")
                    f.write(f"Date Contributed: {date_contributed}\n")
                    f.write(f"Sermon Text:\n{sermon_text}\n")

                print(f"File for {title} by {pastor_name} created successfully.")

if __name__ == "__main__":
    main()

