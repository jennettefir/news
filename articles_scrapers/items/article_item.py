import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose
from articles_scrapers.utils import strip_str


class ArticleItem(scrapy.Item):
    title = scrapy.Field(serializer=str,
                         input_processor=MapCompose(strip_str),
                         output_processor=TakeFirst())
    link = scrapy.Field(serializer=str,
                        output_processor=TakeFirst())
    description = scrapy.Field(serializer=str,
                               input_processor=MapCompose(strip_str),
                               output_processor=TakeFirst())
    author = scrapy.Field(serializer=str,
                          output_processor=TakeFirst())
    text = scrapy.Field(serializer=str,
                        output_processor=TakeFirst())
    text_filepath = scrapy.Field(serializer=str,
                                 output_processor=TakeFirst())
    publication_date = scrapy.Field(serializer=str,
                                    output_processor=TakeFirst())
    guid = scrapy.Field(serializer=str,
                        output_processor=TakeFirst())
    categories = scrapy.Field(serializer=str,
                              output_processor=TakeFirst())
    image_url = scrapy.Field(serializer=str,
                             output_processor=TakeFirst())
    credit = scrapy.Field(serializer=str,
                          output_processor=TakeFirst())
