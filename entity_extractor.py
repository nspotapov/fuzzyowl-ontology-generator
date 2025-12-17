from typing import List, Dict


class EntityExtractor:
    def extract(self, doc) -> List[Dict]:
        results = []

        for token in doc:
            # 1. ADJ + NOUN → нечеткий концепт
            if token.pos_ == "ADJ" and token.head.pos_ == "NOUN":
                results.append(
                    {
                        "type": "fuzzy_concept",
                        "quality": token.lemma_,
                        "entity": token.head.lemma_,
                    }
                )

                # сразу добавляем связь hasQuality
                results.append(
                    {
                        "type": "relation",
                        "relation": "hasQuality",
                        "from": token.head.lemma_,
                        "to": token.lemma_,
                    }
                )

            # 2. Сущности
            if token.pos_ == "NOUN":
                results.append({"type": "entity", "entity": token.lemma_})

            # 3. Глагол → связь relatedTo
            if token.pos_ == "VERB":
                subjects = [child for child in token.children if child.dep_ == "nsubj"]
                objects = [
                    child for child in token.children if child.dep_ in ("obj", "obl")
                ]

                for subj in subjects:
                    for obj in objects:
                        results.append(
                            {
                                "type": "relation",
                                "relation": "relatedTo",
                                "from": subj.lemma_,
                                "to": obj.lemma_,
                            }
                        )

        return results
