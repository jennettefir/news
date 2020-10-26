import database.queries as query


class SaveArticlePipeline:

    def process_item(self, item, spider):
        if item:
            query.add_article(item)
            return item
