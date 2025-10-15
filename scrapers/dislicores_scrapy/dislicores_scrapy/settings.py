BOT_NAME = "dislicores_scrapy"
SPIDER_MODULES = ["dislicores_scrapy.spiders"]
NEWSPIDER_MODULE = "dislicores_scrapy.spiders"

ROBOTSTXT_OBEY = True
FEEDS = {
    '../../resultados_dislicores.csv': {
        'format': 'csv',
        'overwrite': True
    }
}
