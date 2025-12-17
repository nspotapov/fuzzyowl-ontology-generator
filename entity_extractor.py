from typing import List, Dict


class EntityExtractor:
    def extract(self, doc) -> List[Dict]:
        """
        Извлекает кандидаты в классы онтологии
        """
        entities = []

        for token in doc:
            # прилагательное + существительное
            if token.pos_ == "ADJ" and token.head.pos_ == "NOUN":
                entities.append({"modifier": token.lemma_, "entity": token.head.lemma_})

        return entities
