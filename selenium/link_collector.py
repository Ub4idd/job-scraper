import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Setup paths to save in data/raw
raw_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/raw'))
os.makedirs(raw_dir, exist_ok=True)
csv_path = os.path.join(raw_dir, 'job_links.csv')

# The 3 required sources
urls_to_scrape = [
    "https://boards.greenhouse.io/reddit",
    "https://boards.greenhouse.io/duolingo",
    "https://boards.greenhouse.io/figma"
]

driver = webdriver.Chrome()
all_job_links = []
seen_links = set() # Prevents duplicates

for url in urls_to_scrape:
    print(f"Scanning: {url}")
    driver.get(url)
    time.sleep(4) # Wait for jobs to load on screen

    # Grab all links and filter for job postings
    elements = driver.find_elements(By.TAG_NAME, "a")
    for el in elements:
        try:
            href = el.get_attribute("href")
            if href and "/jobs/" in href and href not in seen_links:
                all_job_links.append({'Job URL': href})
                seen_links.add(href)
        except Exception:
            pass

driver.quit()

# Save to CSV
with open(csv_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Job URL'])
    writer.writeheader()
    writer.writerows(all_job_links)

print(f"Successfully saved {len(all_job_links)} links to job_links.csv!")