BOT_NAME = "jobs_spider"

SPIDER_MODULES = ["jobs_spider.spiders"]
NEWSPIDER_MODULE = "jobs_spider.spiders"

# Spoofs a real Chrome browser to bypass bot blockers
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

ROBOTSTXT_OBEY = False # Set to False to ensure we don't get blocked by strict rules
CONCURRENT_REQUESTS_PER_DOMAIN = 2
DOWNLOAD_DELAY = 1.5 # Slightly higher delay to prevent dropped connections

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"