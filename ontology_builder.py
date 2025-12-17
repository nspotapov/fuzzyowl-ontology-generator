from owlready2 import *
import types


class OntologyBuilder:
    def __init__(self, iri="http://example.org/fuzzy.owl"):
        self.onto = get_ontology(iri)

        with self.onto:

            class Entity(Thing):
                pass

            class Quality(Thing):
                pass

            class FuzzyConcept(Thing):
                pass

            class fuzzyDegree(AnnotationProperty):
                pass

    def build(self, extracted, fuzzy_mapper):
        for item in extracted:

            if item["type"] == "fuzzy_concept":
                quality = item["quality"]
                entity = item["entity"]

                degree = fuzzy_mapper.map(quality)
                if degree is None:
                    continue

                class_name = f"{quality.capitalize()}{entity.capitalize()}"

                with self.onto:
                    cls = types.new_class(class_name, (self.onto.FuzzyConcept,))
                    cls.fuzzyDegree.append(degree)
                    cls.comment.append(f"Нечеткий концепт: {quality} {entity}")

            elif item["type"] == "entity":
                class_name = item["entity"].capitalize()
                with self.onto:
                    types.new_class(class_name, (self.onto.Entity,))

    def save(self, path="data/fuzzy.owl"):
        self.onto.save(file=path, format="rdfxml")
