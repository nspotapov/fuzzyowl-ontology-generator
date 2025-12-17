from nlp_processor import NLPProcessor
from entity_extractor import EntityExtractor
from fuzzy_mapper import FuzzyMapper
from ontology_builder import OntologyBuilder


def main():
    text = """
    Система сильно влияет на надежность
    """

    nlp = NLPProcessor()
    extractor = EntityExtractor()
    fuzzy_mapper = FuzzyMapper()
    builder = OntologyBuilder()

    doc = nlp.process(text)
    entities = extractor.extract(doc)

    builder.build(entities, fuzzy_mapper)
    builder.save()

    print("FuzzyOWL-онтология успешно создана")


if __name__ == "__main__":
    main()
