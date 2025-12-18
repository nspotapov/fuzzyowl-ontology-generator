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

            class FuzzyRelation(Thing):
                pass

            class FuzzyQualityRelation(Thing):
                pass

            # ---------- Object properties ----------

            class hasSource(ObjectProperty):
                domain = [FuzzyRelation]
                range = [Thing]

            class hasTarget(ObjectProperty):
                domain = [FuzzyRelation]
                range = [Thing]

            class fqHasSource(ObjectProperty):
                domain = [FuzzyQualityRelation]
                range = [Entity]

            class fqHasQuality(ObjectProperty):
                domain = [FuzzyQualityRelation]
                range = [Quality]

            # ---------- Fuzzy annotation ----------

            class fuzzyDegree(AnnotationProperty):
                pass

        # ---------- Save references ----------
        self.Entity = self.onto.Entity
        self.Quality = self.onto.Quality
        self.FuzzyRelation = self.onto.FuzzyRelation
        self.FuzzyQualityRelation = self.onto.FuzzyQualityRelation

    def get_or_create_class(self, name, base):
        if name not in self.created_classes:
            with self.onto:
                cls = type(name, (base,), {})
            self.created_classes[name] = cls
        return self.created_classes[name]

    def build(self, extracted, fuzzy_mapper):
        for item in extracted:

            modifier = item.get("modifier")
            degree = fuzzy_mapper.map(modifier) if modifier else None

            # ---------- Entity ----------
            if item["type"] == "entity":
                self.get_or_create_class(item["entity"].capitalize(), self.Entity)

            # ---------- Quality ----------
            elif item["type"] == "quality":
                self.get_or_create_class(item["quality"].capitalize(), self.Quality)

            # ---------- Fuzzy quality relation ----------
            elif item["type"] == "relation":
                from_cls = self.get_or_create_class(
                    item["from"].capitalize(), self.Entity
                )
                to_cls = self.get_or_create_class(item["to"].capitalize(), self.Quality)

                fq = self.FuzzyQualityRelation()
                fq.fqHasSource.append(from_cls)
                fq.fqHasQuality.append(to_cls)

                if degree is not None:
                    fq.fuzzyDegree.append(degree)

            # ---------- Fuzzy relation ----------
            elif item["type"] == "fuzzy_relation":
                from_cls = self.get_or_create_class(
                    item["from"].capitalize(), self.Entity
                )

                # цель может быть и Entity, и Quality
                to_base = (
                    self.Quality
                    if item.get("target_type") == "quality"
                    else self.Entity
                )
                to_cls = self.get_or_create_class(item["to"].capitalize(), to_base)

                fr = self.FuzzyRelation()
                fr.hasSource.append(from_cls)
                fr.hasTarget.append(to_cls)

                if degree is not None:
                    fr.fuzzyDegree.append(degree)

    def save(self, path=None):
        if path is None:
            path = f"data/fuzzy-{str(uuid.uuid4())[:8]}.owl"

        self.onto.save(file=path, format="rdfxml")
