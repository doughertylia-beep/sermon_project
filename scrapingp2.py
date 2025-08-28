#PART 2: FILTERING LINKS

#excluding pastors without addresses

#inout: pastor_links in temp folder
#output: filtered_pastor_links in temp folder

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import csv


def load_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        print("File successfully loaded into DataFrame.")
        return df
    except FileNotFoundError:
        print("File path is invalid or the file does not exist.")
        return None

def get_soup(url):
    print("Fetching URL:", url)
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Failed to fetch or parse {url}: {e}")
        return None

#getting address
def get_address(soup):
    legend_tag = soup.find('legend', string=re.compile(r"'s church", re.IGNORECASE))
    if legend_tag:
        p_tag = legend_tag.find_next_sibling('p')
        if p_tag:
            address_info = p_tag.get_text(separator='\n').strip()
            address_lines = address_info.split('\n')[1:-1] 
            cleaned_address = '\n'.join(address_lines).strip()
            if cleaned_address:
                return cleaned_address
    return None

#filtering links based on address existing
def filter_pastor_links(df):
    filtered_links = []

    for index, row in df.iterrows():
        url = row['Link']
        soup = get_soup(url)
        if soup:
            church_address = get_address(soup)
            # if an address is found, add the link to the filtered list
            if church_address is not None:
                filtered_links.append(url)

    return filtered_links

def main():

    desktop_path = '/Users/liadougherty/Desktop/temp'
    os.makedirs(desktop_path, exist_ok=True)  

    input_file_path = os.path.join(desktop_path, "pastor_links.csv")
    output_file_path = os.path.join(desktop_path, "filtered_pastor_links.csv")

    df = load_csv(input_file_path)
    if df is not None:

        filtered_links = filter_pastor_links(df)

        try:
            with open(output_file_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['Link'])  
                for link in filtered_links:
                    csvwriter.writerow([link])
            print(f"Filtered links have been saved to {output_file_path}")
        except Exception as e:
            print(f"Failed to write to {output_file_path}: {e}")

if __name__ == "__main__":
    main()
