from owlready2 import *
import uuid
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

            class hasQuality(ObjectProperty):
                domain = [Entity]
                range = [Quality]

            class relatedTo(ObjectProperty):
                domain = [Entity]
                range = [Entity]

            class fuzzyDegree(AnnotationProperty):
                pass

    def get_or_create_class(self, name, base):
        if name not in self.created_classes:
            self.created_classes[name] = types.new_class(name, (base,))
        return self.created_classes[name]

    def build(self, extracted, fuzzy_mapper):
        for item in extracted:

            # 1. Сущности
            if item["type"] == "entity":
                self.get_or_create_class(item["entity"].capitalize(), self.onto.Entity)

            # 2. Нечеткие концепты
            elif item["type"] == "fuzzy_concept":
                quality = item["quality"]
                entity = item["entity"]

                degree = fuzzy_mapper.map(quality)
                if degree is None:
                    continue

                class_name = f"{quality.capitalize()}{entity.capitalize()}"
                cls = self.get_or_create_class(class_name, self.onto.FuzzyConcept)

                cls.fuzzyDegree.append(degree)
                cls.comment.append(f"Нечеткий концепт: {quality} {entity}")

            # 3. ObjectProperty
            elif item["type"] == "relation":
                from_cls = self.get_or_create_class(
                    item["from"].capitalize(), self.onto.Entity
                )

                # hasQuality → Quality
                if item["relation"] == "hasQuality":
                    to_cls = self.get_or_create_class(
                        item["to"].capitalize(), self.onto.Quality
                    )
                    from_cls.hasQuality.append(to_cls)

                # relatedTo → Entity
                elif item["relation"] == "relatedTo":
                    to_cls = self.get_or_create_class(
                        item["to"].capitalize(), self.onto.Entity
                    )
                    from_cls.relatedTo.append(to_cls)

    def save(self, path=f"data/fuzzy-{str(uuid.uuid4())[:8]}.owl"):
        self.onto.save(file=path, format="rdfxml")
