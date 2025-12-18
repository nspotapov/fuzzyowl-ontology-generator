import argparse
from pathlib import Path

from nlp_processor import NLPProcessor
from entity_extractor import EntityExtractor
from fuzzy_mapper import FuzzyMapper
from ontology_builder import OntologyBuilder


def read_input_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Входной файл не найден: {path}")
    return path.read_text(encoding="utf-8")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Генератор FuzzyOWL-онтологии из текста"
    )

    parser.add_argument(
        "-i", "--input", required=True, help="Путь к входному текстовому файлу"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="fuzzy.owl",
        help="Путь к выходному OWL-файлу (по умолчанию fuzzy.owl)",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    text = read_input_text(input_path)

    nlp = NLPProcessor()
    extractor = EntityExtractor()
    fuzzy_mapper = FuzzyMapper()
    builder = OntologyBuilder()

    doc = nlp.process(text)
    extracted = extractor.extract(doc)

    builder.build(extracted, fuzzy_mapper)
    builder.save(str(output_path))

    print("Онтология успешно создана")
    print(f"Входной файл: {input_path}")
    print(f"Выходной файл: {output_path}")


if __name__ == "__main__":
    main()
