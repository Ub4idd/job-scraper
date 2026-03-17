# Job Market Scraper and Workforce Analyzer

An end-to-end data engineering pipeline designed to automate the collection, extraction, and analysis of job market data. This project targets tech roles across major companies (Reddit, Figma, Duolingo) by combining browser automation with high-speed asynchronous web crawling.

## Project Overview

Modern job boards often use dynamic JavaScript rendering and anti-bot measures to obscure data. This scraper bypasses those limitations by utilizing a two-phase architecture:
1.  **Link Discovery:** A headless Selenium browser mimics human scrolling behavior to bypass lazy-loading and gather complete job URL lists.
2.  **Deep Extraction:** A Scrapy spider visits each URL, parsing hidden JSON-LD metadata and utilizing regex to reliably extract 10 specific data points, even when standard HTML text is blocked.

## Technical Stack

* **Language:** Python 3.x
* **Web Automation:** Selenium WebDriver
* **Data Extraction:** Scrapy
* **Data Processing:** Pandas
* **Visualization:** Matplotlib

## Core Features

* **Anti-Blocking Mechanisms:** Utilizes User-Agent spoofing and intelligent request delays.
* **JSON-LD Parsing:** Bypasses "Enable JavaScript" blocks by reading SEO-optimized hidden script tags.
* **Regex Salary Scanner:** Automatically identifies and extracts salary ranges hidden within unstructured paragraph text.
* **Automated Analytics:** Generates a statistical terminal report and four distinct visual charts outlining hiring trends, top skills, and entry-level role availability.

## Project Structure

* `/selenium`: Contains the initial web automation script to harvest job URLs.
* `/scrapy_project`: Contains the customized Scrapy spider, middleware, and settings.
* `/data`: Houses the raw URL feeds and the final processed `jobs.csv` dataset.
* `/analysis`: Contains the Pandas/Matplotlib script and the generated `.png` charts.

## Execution Pipeline

To run this project from scratch, execute the following commands in order:

**1. Collect Links (Selenium)**
```bash
python selenium/link_collector.py
