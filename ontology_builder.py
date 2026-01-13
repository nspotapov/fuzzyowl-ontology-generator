# ./ontology_builder.py

import datetime
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

            class Entity(Thing):
                pass

            class Quality(Thing):
                pass

            class FuzzyRelation(Thing):
                pass

            class FuzzyQualityRelation(Thing):
                pass

            class hasSource(ObjectProperty):
                domain = [FuzzyRelation]
                range = [Thing]

            class hasTarget(ObjectProperty):
                domain = [FuzzyRelation]
                range = [Thing]

            class fqHasSource(ObjectProperty):
                domain = [FuzzyQualityRelation]
                range = [Thing]

            class fqHasQuality(ObjectProperty):
                domain = [FuzzyQualityRelation]
                range = [Quality]

            class fuzzyDegree(AnnotationProperty):
                pass

        self.Entity = self.onto.Entity
        self.Quality = self.onto.Quality
        self.FuzzyRelation = self.onto.FuzzyRelation
        self.FuzzyQualityRelation = self.onto.FuzzyQualityRelation

    def get_or_create_class(self, name, base):
        name = name.replace(" ", "_")
        if name not in self.created_classes:
            with self.onto:
                cls = type(name, (base,), {})
            self.created_classes[name] = cls
        return self.created_classes[name]

    def build(self, extracted):
        for item in extracted:

            degree = item.get("degree")

            source_base = (
                self.Entity if item["source_type"] == "entity" else self.Quality
            )
            target_base = (
                self.Entity if item["target_type"] == "entity" else self.Quality
            )

            source_cls = self.get_or_create_class(item["source"], source_base)
            target_cls = self.get_or_create_class(item["target"], target_base)

            # ---------- Entity → Entity ----------
            if (
                item["type"] == "fuzzy_relation"
                and item["source_type"] == "entity"
                and item["target_type"] == "entity"
            ):
                fr = self.FuzzyRelation()
                fr.hasSource.append(source_cls)
                fr.hasTarget.append(target_cls)

                if degree is not None:
                    fr.fuzzyDegree.append(degree)

            # ---------- Entity/Quality → Quality ----------
            elif item["type"] in ("fuzzy_relation", "fuzzy_quality_relation"):
                fq = self.FuzzyQualityRelation()
                fq.fqHasSource.append(source_cls)
                fq.fqHasQuality.append(target_cls)

                if degree is not None:
                    fq.fuzzyDegree.append(degree)

    def save(self, path=None):
        if path is None:
            path = f"data/fuzzy-{int(datetime.datetime.now().timestamp())}.owl"

        self.onto.save(file=path, format="rdfxml")
