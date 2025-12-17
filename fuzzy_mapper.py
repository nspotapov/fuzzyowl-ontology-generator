class FuzzyMapper:
    def __init__(self):
        self.linguistic_scale = {
            "очень низкий": 0.1,
            "низкий": 0.3,
            "средний": 0.5,
            "высокий": 0.7,
            "очень высокий": 0.9,
            "малый": 0.3,
            "большой": 0.7,
            "значительный": 0.8,
            "незначительный": 0.2,
        }

    def map(self, quality: str):
        return self.linguistic_scale.get(quality)
