# ./entity_extractor.py


class EntityExtractor:
    def __init__(self):
        self.fuzzy_map = {
            "очень": 0.9,
            "сильно": 0.8,
            "высокий": 0.7,
            "высокая": 0.7,
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

            degree = None
            for t in tokens:
                if t.lemma_.lower() in self.fuzzy_map:
                    degree = self.fuzzy_map[t.lemma_.lower()]

            # ---------- поиск глагола ----------
            verb = next(
                (
                    t
                    for t in tokens
                    if t.pos_ == "VERB" and t.lemma_.lower() in self.relation_verbs
                ),
                None,
            )

            if not verb:
                continue

            # ---------- источник ----------
            source = next(
                (t for t in tokens if t.dep_ in {"nsubj", "nsubj:pass"}), None
            )

            # ---------- цель ----------
            target = next((t for t in tokens if t.dep_ in {"obj", "obl"}), None)

            if not source or not target:
                continue

            source_type = (
                "quality" if source.lemma_.lower() in self.quality_words else "entity"
            )

            target_type = (
                "quality" if target.lemma_.lower() in self.quality_words else "entity"
            )

            results.append(
                {
                    "type": "fuzzy_relation",
                    "source": source.lemma_.capitalize(),
                    "source_type": source_type,
                    "target": target.lemma_.capitalize(),
                    "target_type": target_type,
                    "degree": degree,
                }
            )

        return results
