from scrapy.cmdline import execute
import os,sys


sys.path.append(os.path.abspath( os.path.dirname(__file__)))

#execute('scrapy crawl luoxiaxiaoshuo'.split())
execute('scrapy crawl jb51'.split())
