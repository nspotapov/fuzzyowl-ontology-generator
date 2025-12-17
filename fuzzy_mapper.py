class FuzzyMapper:
    def __init__(self):
        self.linguistic_scale = {
            # качества
            "очень низкий": 0.1,
            "низкий": 0.3,
            "средний": 0.5,
            "высокий": 0.7,
            "очень высокий": 0.9,
            # отношения
            "слабо": 0.3,
            "умеренно": 0.5,
            "сильно": 0.9,
            "возможно": 0.4,
        }

    def map(self, word: str):
        return self.linguistic_scale.get(word)
