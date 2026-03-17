import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

print("Starting the Selenium Robot...")

# 1. Setup Chrome options to act exactly like a human
chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)

# 2. The Target Companies
urls = {
    "Reddit": "https://boards.greenhouse.io/reddit",
    "Figma": "https://boards.greenhouse.io/figma",
    "Duolingo": "https://careers.duolingo.com/jobs"
}

all_links = []

# 3. Visit each site, SCROLL, and collect links
for company_name, url in urls.items():
    print(f"\nScanning {company_name}...")
    driver.get(url)
    
    # Let the initial page load
    time.sleep(3) 
    
    # FORCE SCROLLING: This is the magic fix for Duolingo
    print(f"  -> Scrolling down to load all jobs...")
    for _ in range(4):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2) # Wait for new jobs to pop up after scrolling

    # Find all job links
    links = driver.find_elements(By.TAG_NAME, 'a')
    company_count = 0
    
    for link in links:
        try:
            href = link.get_attribute('href')
            # Check if it's a job link (accounting for different URL structures)
            if href and ('/jobs/' in href or '/roles/' in href or 'gh_jid' in href):
                if href not in all_links:
                    all_links.append(href)
                    company_count += 1
        except:
            continue
            
    print(f"  -> Success! Found {company_count} links for {company_name}.")

driver.quit()

# 4. Save to CSV
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/raw'))
os.makedirs(output_dir, exist_ok=True)
csv_file = os.path.join(output_dir, 'job_links.csv')

with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Job URL'])
    for link in all_links:
        writer.writerow([link])

print(f"\n✅ All done! Saved a total of {len(all_links)} job links to data/raw/job_links.csv")