import scrapy
from scrapy.loader import ItemLoader
from articles_scrapers.items import ArticleItem
from articles_scrapers.utils import text_section_to_text
import articles_scrapers.articles_xpath as xpath


class NyTimesSpider(scrapy.Spider):
    name = 'nytimesbot'
    allowed_domains = ['nytimes.com']

    def start_requests(self):
        rss_feed_urls = self.settings.get('RSS_FEED_URLS', None)
        if rss_feed_urls:
            for url in rss_feed_urls:
                yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        response.selector.remove_namespaces()
        articles = response.xpath(xpath.ARTICLE_ITEM)
        for article in articles:
            article_loader = ItemLoader(item=ArticleItem(), response=response)
            article_loader.selector = article
            article_loader.add_xpath('title', xpath.ARTICLE_TITLE)
            article_link = article.xpath(xpath.ARTICLE_LINK).extract_first()
            article_loader.add_value('link', article_link)
            article_loader.add_xpath('description', xpath.ARTICLE_DESCRIPTION)
            article_author = article.xpath(xpath.ARTICLE_AUTHOR).extract_first()
            if article_author is None:
                article_author = article.xpath(xpath.ARTICLE_AUTHOR_ALTERNATIVE).extract_first()
            article_loader.add_value('author', article_author)
            article_loader.add_xpath('publication_date', xpath.ARTICLE_PUBLICATION_DATE)
            article_categories = " | ".join(article.xpath(xpath.ARTICLE_CATEGORIES).getall())
            article_loader.add_value('categories', article_categories)
            article_loader.add_xpath('image_url', xpath.ARTICLE_IMAGE_URL)
            article_loader.add_xpath('credit', xpath.ARTICLE_CREDIT)
            article_loader.add_xpath('guid', xpath.ARTICLE_GUID)
            article_request = self._create_article_request(article_link, article_loader)
            yield article_request

    def _create_article_request(self, url, article_loader):
        return scrapy.Request(url, callback=self.parse_article, meta={"article_loader": article_loader})

    def parse_article(self, response):
        article_loader = response.meta['article_loader']
        article_body_sections = response.xpath(xpath.ARTICLE_BODY_SECTIONS).getall()
        text_sections = []
        for section in article_body_sections:
            section_selector = scrapy.Selector(text=section)
            paragraphs = section_selector.xpath(xpath.ARTICLE_PARAGRAPHS).getall()
            for paragraph in paragraphs:
                paragraph_selector = scrapy.Selector(text=paragraph)
                text_sections.append("".join(paragraph_selector.css('p ::text').extract()))
        article_loader.add_value('text', text_section_to_text(text_sections))
        yield article_loader.load_item()
