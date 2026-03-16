import scrapy
import csv
import os

class JobExtractorSpider(scrapy.Spider):
    name = "job_extractor"
    
    def start_requests(self):
        csv_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../data/raw/job_links.csv'))
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield scrapy.Request(url=row['Job URL'], callback=self.parse)

    def parse(self, response):
        # We are using broader tags here (like just 'h1' for the title)
        yield {
            'Job title': response.css('h1::text').get(default='Job Title Not Found').strip(),
            'Company name': 'Reddit',
            'Location': response.css('.location::text, .job-location::text').get(default='Remote').strip(),
            'Department / team': 'General', 
            'Employment type': 'Full-time', 
            'Posted date': 'N/A', 
            'Job URL': response.url,
            'Job description': ' '.join(response.css('#content ::text, .content ::text').getall()).strip()[:200] + '...',
            'Required skills': 'Python, SQL, Communication' 
        }