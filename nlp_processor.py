import spacy


class NLPProcessor:
    def __init__(self):
        self.nlp = spacy.load("ru_core_news_sm")

    def process(self, text: str):
        """
        Возвращает spaCy Doc
        """
        return self.nlp(text)
