from owlready2 import *
import types


class OntologyBuilder:
    def __init__(self, iri="http://example.org/fuzzy.owl"):
        self.onto = get_ontology(iri)

        with self.onto:

            class Concept(Thing):
                pass

            # Объявляем аннотационное свойство
            class fuzzyDegree(AnnotationProperty):
                pass

    def build(self, extracted_entities, fuzzy_mapper):
        for item in extracted_entities:
            entity_name = item["entity"].capitalize()
            modifier = item["modifier"]

            fuzzy_value = fuzzy_mapper.map(modifier)
            if fuzzy_value is None:
                continue

            with self.onto:
                cls = types.new_class(entity_name, (self.onto.Concept,))

                # Добавляем аннотацию
                cls.fuzzyDegree.append(fuzzy_value)
                cls.comment.append(
                    f"Нечеткий модификатор: '{modifier}', степень принадлежности = {fuzzy_value}"
                )

    def save(self, path="data/fuzzy.owl"):
        self.onto.save(file=path, format="rdfxml")
