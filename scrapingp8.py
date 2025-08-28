#PART 8
#RECOVERING NA ADDRESSES (requested later)
#RECOVERING "," ADDRESSES (requested later)


#input: pastor_links.csv in temp from part 1
#output: address_pastor_links.csv in temp 

#after this, go through parts 3,(SKIP PART 4),5,6,7 adjusting the inout/output files accordingly


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import csv
import os

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

#filtering links based on address existing or based on "," address
def filter_pastor_links(df):
    filtered_links = []

    for index, row in df.iterrows():
        url = row['Link']
        soup = get_soup(url)
        if soup:
            church_address = get_address(soup)
            #and if no address is found, adding the link to the filtered list
            if church_address is None or church_address == ",":
                filtered_links.append(url)

    return filtered_links

def main():
    desktop_path = '/Users/liadougherty/Desktop/temp'
    input_file_path = os.path.join(desktop_path, "pastor_links.csv")
    output_file_path = os.path.join(desktop_path, "addresses_pastor_links.csv")

    df = load_csv(input_file_path)
    if df is not None:
        filtered_links = filter_pastor_links(df)

        try:
            with open(output_file_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['Link'])  # Writing the header
                for link in filtered_links:
                    csvwriter.writerow([link])
            print(f"Filtered links have been saved to {output_file_path}")
        except Exception as e:
            print(f"Failed to write to {output_file_path}: {e}")

if __name__ == "__main__":
    main()

