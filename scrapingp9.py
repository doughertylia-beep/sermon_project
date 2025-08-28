#PART 9: DATASET

import os
import csv

desktop_path = '/Users/liadougherty/Desktop/temp'
text_files_dir = os.path.join(desktop_path, "sermon_files")


data = []

for filename in os.listdir(text_files_dir):
    if filename.endswith(".txt"):
        with open(os.path.join(text_files_dir, filename), "r", encoding="utf-8") as file:
            content = file.readlines()


            pastor_name = ""
            church_name = ""
            address = ""
            number_of_sermons = ""
            denomination = ""
            title = ""
            date_contributed = ""
            sermon_text = ""
            start_extraction = False

            #processing each line in the file
            for line in content:
                line = line.strip()
                parts = line.split(":", 1)
                if len(parts) == 2 and not start_extraction:
                    attribute_name = parts[0].strip()
                    attribute_value = parts[1].strip()
                    if attribute_name == "Pastor Name":
                        pastor_name = attribute_value
                    elif attribute_name == "Church Name":
                        church_name = attribute_value
                    elif attribute_name == "Address":
                        address = attribute_value
                    elif attribute_name == "Number of Sermons":
                        number_of_sermons = attribute_value
                    elif attribute_name == "Denomination":
                        denomination = attribute_value
                    elif attribute_name == "Title":
                        title = attribute_value
                    elif attribute_name == "Date Contributed":
                        date_contributed = attribute_value
                    elif attribute_name == "Sermon Text":
                        start_extraction = True
                elif start_extraction:
                    if line.strip() or sermon_text:  
                        sermon_text += line + "\n"

            data.append([pastor_name, church_name, address, number_of_sermons, denomination, title, date_contributed, sermon_text.strip()])


csv_file_path = os.path.join(desktop_path, "FULL_DATASET_wtext.csv")

with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "Pastor Name", "Church Name", "Address", "Number of Sermons", "Denomination", "Title", "Date Contributed", "Sermon Text"
    ])
    writer.writerows(data)

print(f"CSV file '{csv_file_path}' has been created.")
