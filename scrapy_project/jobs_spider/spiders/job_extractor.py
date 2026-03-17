import scrapy
import csv
import os
import json
import re
from datetime import datetime

class JobExtractorSpider(scrapy.Spider):
    name = "job_extractor"
    
    def start_requests(self):
        csv_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../data/raw/job_links.csv'))
        if not os.path.exists(csv_file_path):
            self.logger.error("CRITICAL ERROR: job_links.csv not found.")
            return

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # dont_filter=True forces Scrapy to visit EVERY link in your CSV
                yield scrapy.Request(url=row['Job URL'], callback=self.parse, dont_filter=True)

    def parse(self, response):
        url_lower = response.url.lower()
        
        # 1. Company Name
        if 'duolingo' in url_lower:
            company = 'Duolingo'
        elif 'reddit' in url_lower:
            company = 'Reddit'
        elif 'figma' in url_lower:
            company = 'Figma'
        else:
            company = 'Unknown'

        # 2. JSON-LD Extraction
        json_data = response.xpath('//script[@type="application/ld+json"]/text()').get()
        metadata = {}
        if json_data:
            try:
                data = json.loads(json_data)
                metadata = data[0] if isinstance(data, list) else data
            except:
                pass

        # 3. Title
        title = metadata.get('title')
        if not title:
            title = response.css('title::text').get(default='').split('-')[0].replace('Duolingo', '').replace('Figma', '').replace('Reddit', '').strip()
        if not title:
            title = response.css('h1::text').get(default='Job Title Not Found').strip()

        # 4. Location
        location = metadata.get('jobLocation', {}).get('address', {}).get('addressLocality')
        if not location:
            location = response.css('.location::text, .job-location::text').get(default='Remote').strip()

        # 5. Date
        posted_date = metadata.get('datePosted', '').split('T')[0]
        if not posted_date:
            posted_date = datetime.now().strftime('%Y-%m-%d')

        # 6. Description
        raw_text = response.xpath('//body//text()[not(ancestor::script) and not(ancestor::style)]').getall()
        clean_description = ' '.join([t.strip() for t in raw_text if t.strip()])
        if "enable JavaScript" in clean_description or len(clean_description) < 50:
            meta_desc = response.xpath('//meta[@name="description"]/@content').get()
            if meta_desc:
                clean_description = meta_desc

        # 7. Skills
        keywords = ['Python', 'SQL', 'AWS', 'Java', 'Communication', 'Data', 'Agile', 'C++', 'Excel', 'API', 'React', 'Docker']
        found_skills = [skill for skill in keywords if skill.lower() in clean_description.lower()]
        skills_string = ', '.join(found_skills) if found_skills else 'General Skills'

        # 8. Salary
        salary = "Not Disclosed"
        if 'baseSalary' in metadata:
            val = metadata['baseSalary'].get('value', {})
            if isinstance(val, dict):
                min_val = val.get('minValue')
                max_val = val.get('maxValue')
                if min_val and max_val:
                    salary = f"${min_val} - ${max_val}"
                elif min_val:
                    salary = f"${min_val}"
        if salary == "Not Disclosed":
            salary_match = re.search(r'\$[0-9]{2,3},[0-9]{3}(?:\s*-\s*\$[0-9]{2,3},[0-9]{3})?', clean_description)
            if salary_match:
                salary = salary_match.group(0)

        # 9. Yield Final Data
        yield {
            'Job title': title.strip(),
            'Company name': company,
            'Location': location.strip(),
            'Department / team': metadata.get('occupationalCategory', 'Engineering'), 
            'Employment type': metadata.get('employmentType', 'Full-time'), 
            'Posted date': posted_date, 
            'Job URL': response.url,
            'Job description': clean_description[:300] + '...',
            'Required skills': skills_string,
            'Salary': salary
        }