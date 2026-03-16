# Job Market Scraper & Analyzer

## Project Overview
[cite_start]This project is an automated, end-to-end data extraction and analysis pipeline designed to monitor hiring trends by collecting public job listings[cite: 9, 10]. It utilizes a two-part web automation strategy:
1. [cite_start]**Selenium:** Handles user-like browser actions, navigates dynamic job boards, applies an "Engineering" filter, and collects job detail URLs [cite: 15, 26-31].
2. [cite_start]**Scrapy:** Crawls the collected links to extract structured data (Job Title, Location, Skills, Posted Date, etc.) using JSON-LD and XPath parsing [cite: 16, 32-37].
3. [cite_start]**Pandas & Matplotlib:** Analyzes the final dataset and generates a hiring trends report with visual charts[cite: 18, 48].

## Data Source & Compliance
* [cite_start]**Sources:** Public job listings from company careers pages hosted by Greenhouse[cite: 21].
* **Target URLs:** * `https://boards.greenhouse.io/reddit`
  * `https://boards.greenhouse.io/duolingo`
  * `https://boards.greenhouse.io/figma`
* [cite_start]**Compliance:** This scraper accesses public data only, bypasses no CAPTCHAs, requires no authentication, and utilizes respectful request delays to minimize server load [cite: 98-101].

## Repository Structure
* `/selenium/`: Contains `link_collector.py` for browser automation.
* `/scrapy_project/`: Contains the Scrapy spider (`job_extractor.py`) to parse job details.
* [cite_start]`/data/raw/`: Stores the intermediate `job_links.csv` file[cite: 91].
* [cite_start]`/data/final/`: Stores the final extracted dataset `jobs.csv`[cite: 92].
* `/analysis/`: Contains `report.py` to calculate summary metrics and generate PNG charts.
* `/docs/`: Contains the generated charts and project documentation.

## Prerequisites
To run this project, you need Python installed along with the following libraries:
`pip install selenium scrapy pandas matplotlib`

## Usage Instructions
Run the pipeline in the following order from the root directory:

**1. Collect Links (Selenium)**
```bash
python selenium/link_collector.py