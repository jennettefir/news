from __future__ import unicode_literals, print_function
from spacy.lang.en import English


class TextSplitter:
    def __init__(self, text: str):
        self._text = text

    @property
    def text(self):
        return self._text

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def split_to_sentences(self):
        nlp = English()
        nlp.add_pipe(nlp.create_pipe('sentencizer'))  # updated
        doc = nlp(self._text)
        sentences = [sent.string.strip() for sent in doc.sents]
        return sentences

    def split_to_paragraphs(self):
        return [p.strip() for p in self._text.split('\n')]
