import logging
from typing import Optional
from utils import get_logger
from .google_translator import GoogleTranslator
from .bing_translator import BingTranslator
from translate_transition.exceptions import TranslationException
from utils.constants import *
from utils.text_splitter import TextSplitter


class ReWriter:
    DEEPL_ENGINE = DEEPL_ENGINE
    GOOGLE_ENGINE = GOOGLE_ENGINE
    BING_ENGINE = BING_ENGINE

    def __init__(self, origin: str, sequence: Optional[list] = None):
        self._origin = origin
        if sequence is None:
            self._sequence = DEFAULT_SEQUENCE
        else:
            self._sequence = sequence
        self._translation = None

        logging.root.setLevel(logging.NOTSET)
        self.logger = get_logger(self.__class__.__name__)

    @property
    def origin(self):
        return self._origin

    @property
    def sequence(self):
        return self._sequence

    @property
    def translation(self):
        return self._translation

    def rewrite_raw_text(self, text: Optional[str] = None):
        if text is None:
            text = self.origin
        current_text = text
        for index, step in enumerate(self.sequence):
            if step.get("engine") == ReWriter.GOOGLE_ENGINE:
                with GoogleTranslator(current_text, step.get("source", "en"), step.get("target", "en")) as gt:
                    try:
                        current_text = gt.run()
                    except TranslationException as te:
                        self.logger.error(te)
                        raise Exception(f"Failed to complete translation step {index}")
            elif step.get("engine") == ReWriter.BING_ENGINE:
                with BingTranslator(current_text, step.get("source", "en"), step.get("target", "en")) as bt:
                    try:
                        current_text = bt.run()
                    except TranslationException as te:
                        self.logger.error(te)
                        raise Exception(f"Failed to complete translation step {index}")
        return current_text

    def run(self):
        with TextSplitter(self.origin) as text_splitter:
            # sentences = text_splitter.split_to_sentences()
            # re_writen_sentences = []
            # for sentence in sentences:
            #     re_writen_sentences.append(self.rewrite_raw_text(sentence))
            # self._translation = " ".join(re_writen_sentences)

            paragraphs = text_splitter.split_to_paragraphs()
            re_writen_paragraphs = []
            for sentence in paragraphs:
                re_writen_paragraphs.append(self.rewrite_raw_text(sentence))
            self._translation = "\n".join(re_writen_paragraphs)

        return self.translation
