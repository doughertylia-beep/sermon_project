#PART 4: REFINING PASTOR INFO

#filtering out pastors if their addresses is only ","
#differentiating idential pastor names

#input: pastor_info.csv in temp folder
#output: pastor_info2.csv in temp folder

import os
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def main():

    desktop_path = '/Users/liadougherty/Desktop/temp'
    os.makedirs(desktop_path, exist_ok=True)  


    input_file_path = os.path.join(desktop_path, "pastor_infop.csv")
    output_file_path = os.path.join(desktop_path, "pastor_info2.csv")

    try:
        df = pd.read_csv(input_file_path)
        print("File successfully loaded into DataFrame.")
    except FileNotFoundError:
        print("File path is invalid or the file does not exist.")
        return

    #adding count numbers to repeated pastor names
    pastor_counts = {}
    for i, name in enumerate(df['Pastor Name']):
        name_lower = name.lower()  
        if name_lower in pastor_counts:
            pastor_counts[name_lower] += 1
            df.at[i, 'Pastor Name'] = f"{name} {pastor_counts[name_lower]}"
        else:
            pastor_counts[name_lower] = 1

    #searching for addresses that are exactly ","
    rows_with_only_comma = df['Address'] == ','

   #display
    print("Rows to be deleted:")
    print(df[rows_with_only_comma])

    df_cleaned = df[~rows_with_only_comma]

    df_cleaned.to_csv(output_file_path, index=False)
    print(f"Updated data saved to {output_file_path}")

if __name__ == "__main__":
    main()