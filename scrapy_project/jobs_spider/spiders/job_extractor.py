import scrapy
import csv
import os
import json
from datetime import datetime

class JobExtractorSpider(scrapy.Spider):
    name = "job_extractor"
    
    def start_requests(self):
        csv_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../data/raw/job_links.csv'))
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield scrapy.Request(url=row['Job URL'], callback=self.parse)

    def parse(self, response):
        # 1. DATE EXTRACTION: Search hidden JSON-LD first
        posted_date = None
        json_data = response.xpath('//script[@type="application/ld+json"]/text()').get()
        if json_data:
            try:
                data = json.loads(json_data)
                if isinstance(data, list): data = data[0]
                posted_date = data.get('datePosted')
            except:
                pass

        # Fallback to Today if the website doesn't provide a date
        if not posted_date:
            posted_date = datetime.now().strftime('%Y-%m-%d')
        else:
            posted_date = posted_date.split('T')[0]

        # 2. DESCRIPTION: Brute-force body text extraction
        raw_text_pieces = response.xpath('//body//text()[not(ancestor::script) and not(ancestor::style)]').getall()
        clean_description = ' '.join([text.strip() for text in raw_text_pieces if text.strip()])
        
        # 3. SKILL SCANNER: Look for tech keywords in description
        keywords = ['Python', 'SQL', 'AWS', 'Java', 'Communication', 'Data', 'Agile', 'C++', 'Excel', 'API']
        found_skills = [skill for skill in keywords if skill.lower() in clean_description.lower()]
        skills_string = ', '.join(found_skills) if found_skills else 'General Skills'

        # Dynamically get company name from URL (e.g., extracts 'duolingo' from the URL)
        company = response.url.split('/')[3].capitalize()

        # 4. YIELD FINAL DATA
        yield {
            'Job title': response.css('h1::text, .app-title::text').get(default='Job Title Not Found').strip(),
            'Company name': company,
            'Location': response.css('.location::text, .job-location::text').get(default='Remote').strip(),
            'Department / team': 'General', 
            'Employment type': 'Full-time', 
            'Posted date': posted_date, 
            'Job URL': response.url,
            'Job description': clean_description[:500] + '...',
            'Required skills': skills_string 
        }