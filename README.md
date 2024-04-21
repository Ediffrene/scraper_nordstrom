# README: Nordstrom Scraper

Welcome to the Nordstrom Scraper project. This script extracts 120 products from a specified website, providing key product information for further analysis or processing. 
## Prerequisites
- Python 3.x
- Required Python libraries:
  - `time`
  - `selenium.webdriver`
  - `webdriver_manager.chrome`
  - `pyautogui`
  - `pygetwindow`
  - `pyperclip`
  - `random`
  - `bs4`
  - `pickle`
  - `json`
  - `pandas`
  - `xml.etree.ElementTree`

Ensure these libraries are installed before running the script

## Setup and Configuration
1. **Clone or Download the Repository**: Download the script from the repository or copy it to your local environment.
2. **The URL and path**: Edit the script to specify the URL of the website or path to files to scrape. Make sure it's a website that legally allows web scraping.
   - `html_path`: contains a link to a scraping site. Edit if changing the root reference.
   - `vpn_extension_path`: contains the path to the root folder of the browser extension.
   - `site_path`: contains a link to a scraping site.
   - `result_path`: contains the path where the scraping result will be placed.
   - `taxonomy_path`: contains the path where the file with the hierarchical product classification system is located.
4. **Output File**: By default, the script outputs the product data to a XML file. You can modify the output format in the script if needed.

## Usage
To run the script, open a terminal and navigate to the directory containing the script. Then, execute:

```bash
python scraper.py
```

The script will scrape 120 products from the specified website, extract key information according to requirements, and save it to a XML file.

## Disclaimer
This script is provided "as-is" without any warranty. The authors are not responsible for any misuse, data loss, or other issues arising from its use.
