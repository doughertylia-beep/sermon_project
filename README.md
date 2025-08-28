# sermon_project


Guide to Scraping Code Scripts 

Scraping1.py: This part extracts all homepage pastor links. The only requirement is that the pastor has contributed at least 2 sermons.

-	5,534 Pastors
-	15 links per page, 369 pages (checks out sorting by sermons shared= 15*369)
-	Subtracting 1 (last pastor on page 369 who has only contributed 1)
-	input: URL for all pastors 
-	output: pastor_links.csv in temp folder


Scraping2.py: This part filters out unwanted pastor links. We exclude pastors without an address. 

-	4,916 Pastors
-	618 Pastors deleted 
-	input: pastor_links.csv in temp folder
-	output: filtered_pastor_links.csv in temp folder


Scraping3.py:  This part extracts relevant pastor information. Using the home page pastor links, we extract the pastor name, church name, address, num sermons, and denomination and save to a separate csv file.
-	input: filtered_pastor_links.csv in temp folder
-	output: pastor_info.csv in temp folder


Scraping4.py:  This part further trims down the pastor list. We search for “,” addresses and remove the pastor. We also differentiate repeated names. 
-	David Smith, David Smith 2, David Smith 3
-	4,905 Pastors
-	11 Pastors deleted with “,” listed as their address
-	input: pastor_info.csv in temp folder
-	output: pastor_info2.csv in temp folder


Scraping5.py: This part examines each pastor home page link and then compiles a list of all their sermon links (sermon link1, sermon link2, sermon link3, etc) in “SERMON LINKS” variable.
-	Check mechanism to determine if the number of sermon links to scrapes for each pastor’s sermon page MATCHES with the number of sermons reported on a pastor home page
-	Excluding sermon series links too (they lead to a list of sermons in the series, but the individual sermons are also listed on the pastor home page)
-	Excluding links that lead to 404 errors (presumably taken down)
-	input: pastor_info2.csv in temp folder
-	output: pastor_info_wsermons.csv in temp folder


Scraping6.py: This part extracts sermon text and all relevant information and creating sermon files and a folder within temp.
-	Extracting Pastor Name (exactly how they appear in pastor_info_wsermons.csv if there are identical names), Church Name, Address, Denomination, Number of Sermons from  pastor_info_wsermons.csv 
-	Extracting sermon title and text from individual sermon link
-	Storing everything in “sermon_files” within temp folder
-	Input: pastor_info_wsermons.csv in temp folder
-	Output: Individual files labeled as  “{Sermon Title} _ {Pastor Name}.txt” in sermon files folder within temp folder 

Scraping7(1).py: The Duplicate Problem: Since the files were named  “{Sermon Title} _ {Pastor Name},” we realized that if there are multiple sermons from the SAME pastor, the code would skip over the second, third, etc sermon that “technically”  had the same title
-	Went back to the pastor_info_wsermons.csv, which contained the sermon links, retrieved the “title” for each link
-	New column created, “Duplicate Titles,” along with the NUMBER of times it has been repeated
-	New column created, “Duplicate Sermon Links,” which would be the links that were being skipped over in the first iteration of scraping (n-1)
-	If the title has been repeated only twice, the code inserts the second link in this column
-	If the title has been repeated five times, the code inserts the last four links in the column
-	input: pastor_info_wsermons.csv.csv in temp folder
-	output: pastor_info_wsermons_duplicates.csv in temp folder

Scraping7(2).py: The Duplicate Problem: This part creates sermon text files for the skipped over sermon links
-	Returning to Part 6, with the new input file: pastor_info_wsermons_duplicates.csv
-	Changing title of files to be unique urls to avoid duplicate problem again
-	input: pastor_info_wsermons_duplicates.csv in temp folder
-	output: Sermon files.txt labeled as complete URLs in temp folder


Scraping8.py: We realized we might not want to exclude pastors with invalid addresses, so here we add back in the missing addresses (requested later, deleted in part 2) as well as the “,” addresses (deleted in part 4). If this code is replicated, edit out these filtering parts to streamline scrapping processes. 
-	Reversing functionality of PART 2 and PART 4
-	input: pastor_links.csv in temp folder
-	output: address_pastor_links.csv in temp folder
-	Repeating steps 3, 5, 6, 7.1, 7.2, 8
-	Same code used, just changing input file
-	Address_pastor_links.csv (then back to part 3, 5, 6, 7.1, 7.2)
-	Eventually adding these sermons into the temp file


Scraping9.py: Final Dataset: This part uploads all sermon and sermon information into a final dataset.
-	Total number of sermons: 187,706 
-	input: sermon files in temp folder
-	output: FULL_DATASET_wtext.csv in temp folder

