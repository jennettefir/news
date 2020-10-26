import translators as ts
from .base_translator import BaseTranslator
from scrapy.utils.project import get_project_settings
from random import choice


class BingTranslator(BaseTranslator):

    def __init__(self, text: str, source: str, target: str):
        super(BingTranslator, self).__init__(text, source, target)
        self._source = str(source).lower()
        self._target = str(target).lower()

    def run(self):
        if len(self.text.strip()) == 0:
            return ""
        attempt = 0
        while attempt < BingTranslator.MAX_ATTEMPTS:
            attempt += 1
            try:
                return ts.bing(self.text, self.source, self.target, proxies=self.__get_proxies())
            except Exception as _e:
                self.logger.critical(self.text)
                self.logger.critical(_e)
                pass
        else:
            raise Exception(f"Failed to complete translation step")

    def __get_proxies(self):
        proxies = get_project_settings().get("PROXIES", "")
        proxies = proxies.split("\n")
        proxy = choice(proxies) if proxies else None
        if not proxy:
            return {}
        return {"http": proxy, "https": proxy}
