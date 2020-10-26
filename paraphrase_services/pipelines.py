# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
from paraphrase_services.items import QuillBotItem


class ParaphraseServicesPipeline:
    def process_item(self, item, spider):
        return item


class QuillBotPipeline:
    def process_item(self, item, spider):
        if isinstance(item, QuillBotItem):
            source = spider.source
            source_abspath = os.path.abspath(source)
            source_parent_dir = os.path.dirname(source_abspath)
            source_basename = os.path.basename(source_abspath)
            filename_and_ext = os.path.splitext(source_basename)
            target = os.path.join(source_parent_dir, filename_and_ext[0] + '_quill_rewrite' + filename_and_ext[1])
            with open(target, "w+") as target_file:
                target_file.write(dict(item).get("rewritten_text"))
        return item
