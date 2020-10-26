from articles_scrapers.settings import PROXIES
from random import choice


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        proxies = PROXIES
        if proxies is not None:
            proxies = proxies.split("\n")
            request.meta['proxy'] = choice(proxies)
