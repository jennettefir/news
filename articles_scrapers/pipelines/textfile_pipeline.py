import hashlib
from scrapy.utils.python import to_bytes
from scrapy.pipelines.files import FSFilesStore
import os
from datetime import datetime


class TextFilePipeline:

    TEXT_FIELD = 'text'
    TEXT_RESULT_FIELD = 'text_filepath'

    def __init__(self, textfile_store_path):
        self.textfile_store_path = textfile_store_path
        FSFilesStore(textfile_store_path)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            textfile_store_path=crawler.settings.get('TEXTFILE_STORE_PATH', './articles_textfiles')
        )

    def process_item(self, item, spider):
        if item.get('text', None) is not None:
            link = item['link']
            text_filepath = os.path.join(self.textfile_store_path,
                                         f"{datetime.date(datetime.now())}_{self.file_name(link)}")
            with open(text_filepath, 'w', encoding='utf-8') as file_handler:
                file_handler.write(item[self.TEXT_FIELD])
            item[self.TEXT_RESULT_FIELD] = os.path.basename(text_filepath)
            item[self.TEXT_FIELD] = None
            return item

    def file_name(self, link):
        file_guid = hashlib.sha1(to_bytes(link)).hexdigest()
        return f"{file_guid}.txt"

