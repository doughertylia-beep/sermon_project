#PART 7 (1/2)
#DUPLICATES PROBLEM

#if there are multiple sermons with identical titles from the SAME pastor, the code skips over them
#recovering the skipped links here


#input: pastor_info_wsermons.csv in temp
#output: pastor_info_wsermons_duplicates.csv in temp folder

import pandas as pd
import re
from collections import Counter

desktop_path = '/Users/liadougherty/Desktop/temp'


input_file_path = os.path.join(desktop_path, 'pastor_info_wsermons.csv')
output_file_path_duplicates = os.path.join(desktop_path, 'pastor_info_wsermons_duplicates.csv')

df = pd.read_csv(input_file_path)

#normalizing pastor name to help extract title
def normalize_pastor_name(name):
    name = name.lower()
    name = re.sub(r'[^\w\s]', '', name)
    return name

#getting the sermon title from URL
def get_sermon_title(url, name):
    normalized_name = normalize_pastor_name(name)
    path = url.split('/')[-1]
    path_without_params = path.split('?')[0]
    path_segments = url.split('/sermons/')
    if len(path_segments) > 1:
        segment = path_segments[1].split(normalized_name.replace(' ', '-'))[0]
        if segment.endswith('sermon-on'):
            segment = segment[:-9]
        title = segment.replace('-', ' ').title().strip()
        return title
    else:
        return "Title not found"

#getting titles
def extract_titles(row):
    pastor_name = row['Pastor Name']
    sermon_links = row['Sermon Links'].split(',') 
    titles = [get_sermon_title(link, pastor_name) for link in sermon_links]
    return titles, sermon_links

df[['Sermon Titles', 'Sermon Links List']] = df.apply(extract_titles, axis=1, result_type='expand')

#finding duplicate titles and corresponding links within each pastor's sermons
def find_duplicates(titles, links):
    title_counts = Counter(titles)
    duplicates = {title: count for title, count in title_counts.items() if count > 1}
    duplicate_titles_with_counts = [f"{title} ({count})" for title, count in duplicates.items()]
    duplicate_links = []
    for title, count in duplicates.items():
        indices = [i for i, t in enumerate(titles) if t == title]
        if count == 2:
            duplicate_links.append(links[indices[1]])  
        else:
            #saving the last n-1 links (those we have to scrape since the first one has already been scraped)
            duplicate_links.append(','.join(links[i] for i in indices[-(count - 1):])) 
    return duplicate_titles_with_counts, ','.join(duplicate_links) 

df[['Duplicate Titles', 'Duplicate Sermon Links']] = df.apply(
    lambda row: find_duplicates(row['Sermon Titles'], row['Sermon Links List']),
    axis=1, result_type='expand'
)

#filtering out rows without duplicates
df_with_duplicates = df[df['Duplicate Titles'].map(len) > 0]

if not df_with_duplicates.empty:
    df_with_duplicates.to_csv(output_file_path_duplicates, index=False)
    print(f"Analysis complete. Check the '{output_file_path_duplicates}' file for results.")
else:
    print("No duplicate sermon titles found.")




