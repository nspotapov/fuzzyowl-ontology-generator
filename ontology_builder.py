import uuid
from owlready2 import *
import types


class OntologyBuilder:
    def __init__(self, iri="http://example.org/fuzzy.owl"):
        self.onto = get_ontology(iri)
        self.created_classes = {}

        with self.onto:

            class Entity(Thing):
                pass

            class Quality(Thing):
                pass

            class FuzzyConcept(Thing):
                pass

            # 🔥 Рефицированное отношение
            class FuzzyRelation(Thing):
                pass

            class hasSource(ObjectProperty):
                domain = [FuzzyRelation]
                range = [Entity]

            class hasTarget(ObjectProperty):
                domain = [FuzzyRelation]
                range = [Entity]

            class fuzzyDegree(AnnotationProperty):
                pass

    def get_or_create_class(self, name, base):
        if name not in self.created_classes:
            self.created_classes[name] = types.new_class(name, (base,))
        return self.created_classes[name]

    def build(self, extracted, fuzzy_mapper):
        for item in extracted:

            # сущности
            if item["type"] == "entity":
                self.get_or_create_class(item["entity"].capitalize(), self.onto.Entity)

            # нечеткие концепты
            elif item["type"] == "fuzzy_concept":
                degree = fuzzy_mapper.map(item["quality"])
                if degree is None:
                    continue

                cls = self.get_or_create_class(
                    f"{item['quality'].capitalize()}{item['entity'].capitalize()}",
                    self.onto.FuzzyConcept,
                )
                cls.fuzzyDegree.append(degree)

            # обычные отношения
            elif item["type"] == "relation":
                from_cls = self.get_or_create_class(
                    item["from"].capitalize(), self.onto.Entity
                )
                to_cls = self.get_or_create_class(
                    item["to"].capitalize(), self.onto.Quality
                )
                from_cls.hasQuality.append(to_cls)

            elif item["type"] == "fuzzy_relation":
                from_cls = self.get_or_create_class(
                    item["from"].capitalize(), self.onto.Entity
                )
                to_cls = self.get_or_create_class(
                    item["to"].capitalize(), self.onto.Entity
                )

                # создаём экземпляр нечеткого отношения
                fr = self.onto.FuzzyRelation()

                fr.hasSource.append(from_cls)
                fr.hasTarget.append(to_cls)

                if item["modifier"]:
                    degree = fuzzy_mapper.map(item["modifier"])
                    if degree is not None:
                        fr.fuzzyDegree.append(degree)

    def save(self, path=f"data/fuzzy-{str(uuid.uuid4())[:8]}.owl"):
        self.onto.save(file=path, format="rdfxml")
