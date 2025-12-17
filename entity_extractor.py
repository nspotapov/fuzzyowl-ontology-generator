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

                results.append(
                    {
                        "type": "relation",
                        "relation": "hasQuality",
                        "from": token.head.lemma_,
                        "to": token.lemma_,
                        "degree": None,
                    }
                )

            # сущности
            if token.pos_ == "NOUN":
                results.append({"type": "entity", "entity": token.lemma_})

            # Нечеткие глагольные отношения
            if token.pos_ == "VERB":
                adverbs = [c for c in token.children if c.pos_ == "ADV"]
                subjects = [c for c in token.children if c.dep_ == "nsubj"]
                objects = [c for c in token.children if c.dep_ in ("obj", "obl")]

                for subj in subjects:
                    for obj in objects:
                        results.append(
                            {
                                "type": "fuzzy_relation",
                                "relation": "relatedTo",
                                "from": subj.lemma_,
                                "to": obj.lemma_,
                                "modifier": adverbs[0].lemma_ if adverbs else None,
                            }
                        )

        return results
