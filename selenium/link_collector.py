# link_collector.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import os

print("Starting the Selenium Robot...")

# 1. Open Chrome automatically
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 2. Go to an approved public job board (Reddit's Greenhouse board) [cite: 21, 24]
url = "https://boards.greenhouse.io/reddit" 
print(f"Opening website: {url}")
driver.get(url)

# Wait 3 seconds to let the page fully load
time.sleep(3)

# 3. Find and collect all the job detail links [cite: 31]
job_links = []
elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/jobs/']")

for element in elements:
    link = element.get_attribute("href")
    if link not in job_links:
        job_links.append(link)

print(f"Success! Found {len(job_links)} job links.")

# 4. Save these links to your intermediate raw file [cite: 45]
output_path = '../data/raw/job_links.csv'
with open(output_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Job URL'])
    for link in job_links:
        writer.writerow([link])

# Close the browser when finished
driver.quit()
print("Links saved to data/raw/job_links.csv! Phase 2 is complete.")