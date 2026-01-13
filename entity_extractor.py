# ./entity_extractor.py


class EntityExtractor:
    def __init__(self):
        self.fuzzy_map = {
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

    def collect_compound(self, token):
        """
        Собирает составные имена: 'эффективность работы' → Эффективность_Работа
        """
        parts = [token]
        for child in token.children:
            if child.dep_ in {"nmod", "compound"}:
                parts.append(child)
        parts = sorted(parts, key=lambda t: t.i)
        return "_".join(t.lemma_.capitalize() for t in parts)

    def is_quality(self, token):
        """
        Эвристика для качеств (корректно для русского):
        надежность, эффективность, производительность и т.п.
        """
        return token.pos_ == "NOUN" and token.lemma_.lower().endswith("ость")

    def extract(self, doc):
        results = []

        for sent in doc.sents:
            tokens = list(sent)

            # ---------- степень нечеткости ----------
            degree = None
            for t in tokens:
                if t.lemma_.lower() in self.fuzzy_map:
                    degree = self.fuzzy_map[t.lemma_.lower()]

            # ---------- глагол отношения ----------
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

            source_name = self.collect_compound(source)
            target_name = self.collect_compound(target)

            source_type = "quality" if self.is_quality(source) else "entity"
            target_type = "quality" if self.is_quality(target) else "entity"

            results.append(
                {
                    "type": "fuzzy_relation",
                    "source": source_name,
                    "source_type": source_type,
                    "target": target_name,
                    "target_type": target_type,
                    "degree": degree,
                }
            )

        return results
