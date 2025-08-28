# PART 5: GETTING SERMON LINKS

#compling a list of sermon links (sermon link1, sermon link2, sermon link3, etc)

#profile link = https://www.sermoncentral.com/contributors/david-owen-profile-13488
#all sermons link = https://www.sermoncentral.com/contributors/david-owen-sermons-13488
#individual sermon link = https://www.sermoncentral.com/sermons/seek-first-the-kingdom-of-god-david-owen-sermon-on-salvation-171647


#implementing "check" to see if pastor's total number of sermons matches the number of indivudal links found

#input: pastor_info2.csv in temp folder
#output: pastor_info_wsermons.csv in temp folder (list of links that lead to individual sermons to scrape text)

import pandas as pd
import os
import requests
from bs4 import BeautifulSoup

def get_soup(url):
    print("Fetching URL:", url)
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return BeautifulSoup(response.content, 'html.parser')
    except Exception as e:
        print(f"Failed to fetch or parse {url}: {e}")
        return None

def convert_profile_to_sermon(profile_link):
    return profile_link.replace("profile", "sermons")

def get_total_pages(soup):
    page_tags = soup.find_all('a', class_='page')
    if page_tags:
        return max([int(tag.text) for tag in page_tags if tag.text.isdigit()])
    return 1

def extract_sermon_links(soup):
    return [a['href'] for a in soup.find_all('a', href=True) if 'sermon-on' in a['href'] and '/sermon-series/' not in a['href']]

def get_sermon_links(sermon_page_link):
    sermon_links = []
    soup = get_soup(sermon_page_link)
    if not soup:
        return sermon_links

    total_pages = get_total_pages(soup)

    for page_num in range(1, total_pages + 1):
        page_url = f"{sermon_page_link}?page={page_num}"
        soup = get_soup(page_url)
        if not soup:
            continue
        sermon_links.extend(extract_sermon_links(soup))

    return sermon_links

def is_valid_url(url):
    try:
        response = requests.get(url)
        return response.status_code != 404
    except requests.RequestException:
        return False

def main():

    desktop_path = '/Users/liadougherty/Desktop/temp'
    os.makedirs(desktop_path, exist_ok=True)  


    input_file_path = os.path.join(desktop_path, "pastor_infop2.csv")
    output_file_path = os.path.join(desktop_path, "pastor_info_wsermons.csv")
    check_output_file_path = os.path.join(desktop_path, "pastor_info_wsermons_final.csv")

    try:
        df = pd.read_csv(input_file_path)
        print("File successfully loaded into DataFrame.")
    except FileNotFoundError:
        print("File path is invalid or the file does not exist.")
        return

    for index, row in df.iterrows():
        profile_link = row['Filtered Link']
        sermon_link = convert_profile_to_sermon(profile_link)
        sermon_links = get_sermon_links(sermon_link)

        unique_sermon_links = set(sermon_links)

        #prefix to each unique sermon link
        sermon_links_with_prefix = ['https://www.sermoncentral.com' + link for link in unique_sermon_links]

        #number of sermon links
        num_sermon_links = len(sermon_links_with_prefix)

        df.at[index, 'Sermon Links'] = ', '.join(sermon_links_with_prefix)  # Converting list to string

        #comparing number of sermon links with 'Number of Sermons' column
        if num_sermon_links == row['Number of Sermons']:
            df.at[index, 'Check'] = 'Yes'
        else:
            df.at[index, 'Check'] = 'No'

    df.to_csv(output_file_path, index=False)
    print("Updated DataFrame saved to CSV.")

    df = pd.read_csv(output_file_path)

    for index, row in df.iterrows():
        if row['Check'] == "No":
            sermon_links = row['Sermon Links'].split(', ')
            valid_sermon_links = [link for link in sermon_links if is_valid_url(link)]

            df.at[index, 'Sermon Links'] = ', '.join(valid_sermon_links)  
            num_sermon_links = len(valid_sermon_links)

            if num_sermon_links == row['Number of Sermons']:
                df.at[index, 'Check'] = 'Yes'
            else:
                df.at[index, 'Check'] = 'No'

    df.to_csv(check_output_file_path, index=False)
    print("Final updated DataFrame saved to CSV.")

if __name__ == "__main__":
    main()
