class FuzzyMapper:
    def __init__(self):
        self.fuzzy_terms = {
            "низкий": 0.2,
            "малый": 0.3,
            "средний": 0.5,
            "высокий": 0.8,
            "очень высокий": 0.9,
            "пожилой": 0.7,
            "молодой": 0.3,
        }

    def map(self, modifier: str) -> float | None:
        """
        Возвращает степень принадлежности
        """
        return self.fuzzy_terms.get(modifier)
