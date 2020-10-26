from httpx import Client
from googletrans import Translator
from .base_translator import BaseTranslator
from scrapy.utils.project import get_project_settings
from random import choice


class GoogleTranslator(BaseTranslator):
    def __init__(self, text: str, source: str, target: str):
        super(GoogleTranslator, self).__init__(text, source, target)
        self._translator = Translator(proxies=self.__get_proxies())

    def run(self):
        if len(self.text.strip()) == 0:
            return ""
        attempt = 0
        while attempt < GoogleTranslator.MAX_ATTEMPTS:
            attempt += 1
            try:
                translation = self._translator.translate(self.text, src=self.source, dest=self.target)
                current_text = translation.text
                return current_text
            except Exception as _e:
                pass
        else:
            raise Exception(f"Failed to complete translation step")

    def __get_proxies(self):
        proxies = get_project_settings().get("PROXIES", "")
        proxies = proxies.split("\n")
        proxy = choice(proxies) if proxies else None
        if not proxy:
            return {}
        return Client(proxies={"http": proxy, "https": proxy}).proxies
