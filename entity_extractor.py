class EntityExtractor:
    def __init__(self):
        self.fuzzy_map = {
            "сильно": 0.9,
            "высокий": 0.7,
            "высокая": 0.7,
            "высоко": 0.7,
            "умеренно": 0.5,
            "слабо": 0.3,
        }

        self.relation_verbs = {
            "влиять",
            "повышать",
            "увеличивать",
            "снижать",
            "уменьшать",
        }

        self.quality_words = {
            "надежность",
            "эффективность",
            "производительность",
            "стабильность",
            "качество",
        }

    def extract(self, doc):
        results = []

        for sent in doc.sents:
            tokens = list(sent)

            lemmas = [t.lemma_.lower() for t in tokens]

            degree = None
            modifier = None
            for t in tokens:
                if t.lemma_.lower() in self.fuzzy_map:
                    modifier = t.lemma_.lower()
                    degree = self.fuzzy_map[modifier]

            # ----------- нечеткое качество: "Высокая производительность"
            if (
                len(tokens) >= 2
                and tokens[0].pos_ == "ADJ"
                and tokens[1].pos_ in {"NOUN", "PROPN"}
                and tokens[0].lemma_.lower() in self.fuzzy_map
            ):
                results.append(
                    {
                        "type": "fuzzy_quality",
                        "source": tokens[1].lemma_.capitalize(),
                        "target": tokens[0].lemma_.capitalize(),
                        "target_type": "quality",
                        "degree": degree,
                    }
                )

            # ----------- поиск глагола отношения
            verb = None
            for t in tokens:
                if t.pos_ == "VERB" and t.lemma_.lower() in self.relation_verbs:
                    verb = t
                    break

            if not verb:
                continue

            # ----------- источник (подлежащее)
            source = None
            for t in tokens:
                if t.dep_ in {"nsubj", "nsubj:pass"}:
                    source = t
                    break

            # ----------- цель (дополнение)
            target = None
            for t in tokens:
                if t.dep_ in {"obj", "obl"} and t.pos_ in {"NOUN", "PROPN"}:
                    target = t
                    break

            if not source or not target:
                continue

            target_type = (
                "quality" if target.lemma_.lower() in self.quality_words else "entity"
            )

            results.append(
                {
                    "type": "fuzzy_relation" if degree else "relation",
                    "source": source.lemma_.capitalize(),
                    "target": target.lemma_.capitalize(),
                    "target_type": target_type,
                    "degree": degree,
                }
            )

        return results
