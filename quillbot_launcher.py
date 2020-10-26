import sys
import os
from scrapy.cmdline import execute

os.environ['SCRAPY_PROJECT'] = 'paraphrase_services'
os.environ['SCRAPY_SETTINGS_MODULE'] = 'paraphrase_services.settings'

execute(["scrapy", "crawl", "quillbot", "-a", f"source={sys.argv[1]}"])
