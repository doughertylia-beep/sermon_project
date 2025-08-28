# sermon_project

# Guide to Scraping Code Scripts

This repository contains a series of Python scripts used to scrape, filter, and compile sermon data from a pastor directory. The workflow is divided into multiple steps, with each script handling a specific stage in the pipeline.

---

## Overview of Scripts

### Scraping1.py – Extract All Pastor Links
- **Description**: Extracts all homepage pastor links. Pastors must have contributed at least **2 sermons**.  
- **Details**:
  - ~5,534 pastors total  
  - 15 links per page × 369 pages  
  - Final count excludes last pastor with only 1 sermon  
- **Input**: URL for all pastors  
- **Output**: `pastor_links.csv` (in `temp/` folder)  

---

### Scraping2.py – Filter Pastor Links
- **Description**: Removes pastors without an address.  
- **Details**:
  - 4,916 pastors retained  
  - 618 pastors removed  
- **Input**: `pastor_links.csv`  
- **Output**: `filtered_pastor_links.csv`  

---

### Scraping3.py – Extract Pastor Information
- **Description**: Extracts pastor metadata from homepage links:  
  - Name, church name, address, number of sermons, denomination.  
- **Input**: `filtered_pastor_links.csv`  
- **Output**: `pastor_info.csv`  

---

### Scraping4.py – Clean Pastor List
- **Description**: Cleans and deduplicates pastor records.  
  - Removes pastors with `,` in address.  
  - Differentiates repeated names (e.g., *David Smith*, *David Smith 2*, *David Smith 3*).  
- **Details**:
  - 4,905 pastors retained  
  - 11 pastors removed  
- **Input**: `pastor_info.csv`  
- **Output**: `pastor_info2.csv`  

---

### Scraping5.py – Collect Sermon Links
- **Description**: Extracts all sermon links for each pastor.  
  - Verifies sermon count matches reported number.  
  - Excludes **series links** (already included in homepage list).  
  - Excludes **404 errors** (removed sermons).  
- **Input**: `pastor_info2.csv`  
- **Output**: `pastor_info_wsermons.csv`  

---

### Scraping6.py – Extract Sermon Text
- **Description**: Scrapes sermon title and text from individual sermon links.  
  - Saves each sermon as a `.txt` file.  
  - Metadata includes: Pastor name, church name, address, denomination, number of sermons.  
- **Input**: `pastor_info_wsermons.csv`  
- **Output**: Individual sermon files in `sermon_files/` inside `temp/`  

---

### Scraping7(1).py – Handle Duplicate Titles (Detection)
- **Description**: Identifies duplicate sermon titles per pastor (causing skipped scrapes).  
  - Adds column **Duplicate Titles** (count of repetitions).  
  - Adds column **Duplicate Sermon Links** (skipped links).  
- **Input**: `pastor_info_wsermons.csv`  
- **Output**: `pastor_info_wsermons_duplicates.csv`  

---

### Scraping7(2).py – Handle Duplicate Titles (File Creation)
- **Description**: Creates sermon files for duplicate links.  
  - File names changed to **unique URLs** to prevent overwriting.  
- **Input**: `pastor_info_wsermons_duplicates.csv`  
- **Output**: Sermon text files (URLs as filenames) in `temp/`  

---

### Scraping8.py – Re-Include Removed Addresses
- **Description**: Restores pastors excluded in earlier steps:  
  - Adds back pastors without addresses (removed in Step 2).  
  - Adds back pastors with `,` addresses (removed in Step 4).  
- **Workflow**:  
  - Reverse Steps 2 and 4 → repeat Steps 3, 5, 6, 7.1, 7.2, 8.  
  - Sermons added into `temp/` alongside others.  
- **Input**: `pastor_links.csv`  
- **Output**: `address_pastor_links.csv`  

---

### Scraping9.py – Final Dataset Creation
- **Description**: Combines all sermons and metadata into the final dataset.  
- **Details**:
  - **Total sermons**: 187,706  
- **Input**: Sermon text files in `temp/`  
- **Output**: `FULL_DATASET_wtext.csv`  

---

## Final Notes
- All intermediate and final files are stored in the **`temp/` folder**.  
- Duplicate handling ensures **no sermons are skipped**.  
- Steps 8–9 provide flexibility if different filtering criteria are applied.  
