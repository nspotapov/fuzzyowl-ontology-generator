import uuid
from owlready2 import (
    get_ontology,
    Thing,
    ObjectProperty,
    AnnotationProperty,
)


class OntologyBuilder:
    def __init__(self, iri="http://example.org/fuzzy.owl"):
        self.onto = get_ontology(iri)
        self.created_classes = {}

        with self.onto:
            # ---------- Base classes ----------

            class Entity(Thing):
                pass

            class Quality(Thing):
                pass

            class FuzzyConcept(Thing):
                pass

            class FuzzyRelation(Thing):
                pass

            # ---------- Object properties ----------

            class hasQuality(ObjectProperty):
                domain = [Entity]
                range = [Quality]

            class hasSource(ObjectProperty):
                domain = [FuzzyRelation]
                range = [Thing]

            class hasTarget(ObjectProperty):
                domain = [FuzzyRelation]
                range = [Thing]

            # ---------- Fuzzy annotation ----------

            class fuzzyDegree(AnnotationProperty):
                pass

        self.Entity = self.onto.Entity
        self.Quality = self.onto.Quality
        self.FuzzyConcept = self.onto.FuzzyConcept
        self.FuzzyRelation = self.onto.FuzzyRelation

    def get_or_create_class(self, name, base):
        """
        Создаёт или возвращает OWL-класс в онтологии
        """
        if name not in self.created_classes:
            with self.onto:
                cls = type(name, (base,), {})
            self.created_classes[name] = cls
        return self.created_classes[name]

    def build(self, extracted, fuzzy_mapper):
        """
        Строит онтологию на основе извлечённых сущностей и отношений
        """
        for item in extracted:

            # ---------- Entity ----------
            if item["type"] == "entity":
                self.get_or_create_class(item["entity"].capitalize(), self.Entity)

            # ---------- Fuzzy concept ----------
            elif item["type"] == "fuzzy_concept":
                degree = fuzzy_mapper.map(item["quality"])
                if degree is None:
                    continue

                cls = self.get_or_create_class(
                    f"{item['quality'].capitalize()}{item['entity'].capitalize()}",
                    self.FuzzyConcept,
                )
                cls.fuzzyDegree.append(degree)

            # ---------- Quality relation ----------
            elif item["type"] == "relation":
                from_cls = self.get_or_create_class(
                    item["from"].capitalize(), self.Entity
                )
                to_cls = self.get_or_create_class(item["to"].capitalize(), self.Quality)
                from_cls.hasQuality.append(to_cls)

            # ---------- Fuzzy relation ----------
            elif item["type"] == "fuzzy_relation":
                from_cls = self.get_or_create_class(
                    item["from"].capitalize(), self.Entity
                )
                to_cls = self.get_or_create_class(item["to"].capitalize(), self.Entity)

                fr = self.FuzzyRelation()
                fr.hasSource.append(from_cls)
                fr.hasTarget.append(to_cls)

                if item.get("modifier"):
                    degree = fuzzy_mapper.map(item["modifier"])
                    if degree is not None:
                        fr.fuzzyDegree.append(degree)

    def save(self, path=None):
        """
        Сохраняет онтологию в OWL-файл
        """
        if path is None:
            path = f"data/fuzzy-{str(uuid.uuid4())[:8]}.owl"

        self.onto.save(file=path, format="rdfxml")
