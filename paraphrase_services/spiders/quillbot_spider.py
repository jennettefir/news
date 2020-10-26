import os
import re
import json
import scrapy
from scrapy.exceptions import CloseSpider
from furl import furl
from utils.text_splitter import TextSplitter
from paraphrase_services.items import QuillBotItem


class QuillBotSpider(scrapy.Spider):
    name = "quillbot"

    custom_settings = {
        "ITEM_PIPELINES": {
            "paraphrase_services.pipelines.QuillBotPipeline": 300,
        },
        "LOG_LEVEL": "ERROR",
    }

    def __init__(self, *args, **kwargs):
        super(QuillBotSpider, self).__init__(*args, **kwargs)
        self.source = kwargs.get("source", None)
        self.is_flip_enabled = True

    def start_requests(self):
        if self.source is not None:
            if not os.path.exists(self.source):
                raise CloseSpider("Source file to paraphrase does not exist")
            with open(self.source, 'r') as source_file:
                source_text = source_file.read().strip()
                yield scrapy.Request("https://www.quillbot.com/", callback=self.collect_cookies,
                                     cb_kwargs={"source_text": source_text})
        else:
            raise CloseSpider("Source file to paraphrase does not provided")

    def _build_single_paraphrase_request(self, sentences, current_sentence, paraphrase_sentences):
        f = furl("https://www.quillbot.com/api/singleParaphrase/2")
        f.set({
            "userID": "N/A",
            "text": sentences[current_sentence],
            "strength": 2,
            "autoflip": False,
            "wikify": False,
            "fthresh": -1
        })
        return scrapy.Request(f.url, callback=self.parse_single_paraphrase,
                              cb_kwargs={
                                  "sentences": sentences,
                                  "current_sentence": current_sentence,
                                  "paraphrase_sentences": paraphrase_sentences
                              })

    def _build_single_flip_request(self, sentences, current_sentence, paraphrase_sentences, flipped_sentences):
        f = furl("https://www.quillbot.com/api/singleFlip")
        f.set({
            "userID": "N/A",
            "text": sentences[current_sentence],
            "alt": paraphrase_sentences[current_sentence],
            "fthresh": 9
        })
        return scrapy.Request(f.url, callback=self.parse_single_flip,
                              cb_kwargs={
                                  "sentences": sentences,
                                  "current_sentence": current_sentence,
                                  "paraphrase_sentences": paraphrase_sentences,
                                  "flipped_sentences": flipped_sentences
                              })

    def collect_cookies(self, response, source_text):
        self.logger.debug(response.status)
        with TextSplitter(source_text) as text_splitter:
            sentences = text_splitter.split_to_sentences()
            current_sentence = 0
            paraphrase_sentences = []
            yield self._build_single_paraphrase_request(sentences, current_sentence, paraphrase_sentences)

    def parse_single_paraphrase(self, response, sentences, current_sentence, paraphrase_sentences):
        json_response = json.loads(response.body)
        alt_paraphrase = ""
        max_score = None
        for key, value in json_response[0].items():
            # if "paras_" in key:
            if "paras_3" in key:
                for paraphrase in value:
                    if max_score is None or paraphrase["score"] > max_score:
                        max_score = paraphrase["score"]
                        alt_paraphrase = paraphrase["alt"]

        paraphrase_sentences.append(alt_paraphrase)
        if current_sentence != len(sentences) - 1:
            yield self._build_single_paraphrase_request(sentences, current_sentence + 1, paraphrase_sentences)
        else:
            if self.is_flip_enabled:
                current_sentence = 0
                flipped_sentences = []
                yield self._build_single_flip_request(sentences, current_sentence, paraphrase_sentences,
                                                      flipped_sentences)
            else:
                yield QuillBotItem({"rewritten_text": "\n".join(paraphrase_sentences)})

    def parse_single_flip(self, response, sentences, current_sentence, paraphrase_sentences, flipped_sentences):
        json_response = json.loads(response.body)
        flipped_paraphrase = json_response.get("flipped_alt")
        if len(str(flipped_paraphrase)) and str(flipped_paraphrase).islower():
            yield response.request.copy().replace(dont_filter=True)
            return
        if len(str(flipped_paraphrase)) == 0:
            yield response.request.copy().replace(dont_filter=True)
            return
        for key, values in dict(json_response.get("walts", {})).items():
            if key != key.encode('ascii', errors='ignore').decode():
                first_correct_value = ""
                for value in values:
                    if value == value.encode('ascii', errors='ignore').decode():
                        first_correct_value = value
                        break
                key_to_delete = str(key.split('~')[0]).lower()
                flipped_paraphrase_lower = str(flipped_paraphrase).lower()

                key_to_delete_index = flipped_paraphrase_lower.find(key_to_delete)
                while key_to_delete_index != -1:
                    flipped_paraphrase = flipped_paraphrase[:key_to_delete_index] + \
                                         first_correct_value + \
                                         flipped_paraphrase[key_to_delete_index+len(key_to_delete):]
                    flipped_paraphrase_lower = flipped_paraphrase.lower()
                    key_to_delete_index = flipped_paraphrase_lower.find(key_to_delete)

                flipped_paraphrase.replace(key.split('~')[0], first_correct_value)
                flipped_paraphrase.replace(key.split('~')[0].upper(), first_correct_value)
        flipped_sentences.append(flipped_paraphrase)
        if current_sentence != len(sentences) - 1:
            yield self._build_single_flip_request(sentences, current_sentence + 1, paraphrase_sentences,
                                                  flipped_sentences)
        else:
            yield QuillBotItem({"rewritten_text": "\n".join(flipped_sentences)})

    def parse(self, response):
        pass
