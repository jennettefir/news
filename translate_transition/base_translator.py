from utils import get_logger


class BaseTranslator:
    MAX_ATTEMPTS = 3

    def __init__(self, text: str, source: str, target: str):
        self._text = text
        self._source = source
        self._target = target

        self.logger = get_logger(self.__class__.__name__)

    @property
    def text(self):
        return self._text

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def run(self):
        raise NotImplemented
