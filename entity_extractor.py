from typing import List, Dict


class EntityExtractor:
    def extract(self, doc) -> List[Dict]:
        results = []

        for token in doc:
            # ADJ + NOUN → нечеткий концепт
            if token.pos_ == "ADJ" and token.head.pos_ == "NOUN":
                results.append(
                    {
                        "type": "fuzzy_concept",
                        "quality": token.lemma_,
                        "entity": token.head.lemma_,
                    }
                )

            # одиночные сущности
            if token.pos_ == "NOUN":
                results.append({"type": "entity", "entity": token.lemma_})

        return results
