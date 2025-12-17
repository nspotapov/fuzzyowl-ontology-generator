from owlready2 import *


class OntologyBuilder:
    def __init__(self, iri="http://example.org/fuzzy.owl"):
        self.onto = get_ontology(iri)

    def build(self, extracted_entities, fuzzy_mapper):
        with self.onto:

            class Concept(Thing):
                pass

        for item in extracted_entities:
            entity_name = item["entity"].capitalize()
            modifier = item["modifier"]

            fuzzy_value = fuzzy_mapper.map(modifier)
            if fuzzy_value is None:
                continue

            with self.onto:
                cls = types.new_class(entity_name, (Concept,))
                cls.comment.append(
                    f"Нечеткий модификатор: {modifier}, степень = {fuzzy_value}"
                )
                cls.fuzzyDegree = fuzzy_value

    def save(self, path="fuzzy.owl"):
        self.onto.save(file=path, format="rdfxml")
