# ./main.py

import argparse
from pathlib import Path

from nlp_processor import NLPProcessor
from entity_extractor import EntityExtractor
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
        default=None,
        help="Путь к выходному OWL-файлу",
    )

    return parser.parse_args()


def normalize_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return ". ".join(lines) + "."


def main():
    args = parse_args()

    text = read_input_text(Path(args.input))

    text = normalize_text(text)

    nlp = NLPProcessor()
    extractor = EntityExtractor()
    builder = OntologyBuilder()

    doc = nlp.process(text)
    extracted = extractor.extract(doc)

    builder.build(extracted)
    save_path = builder.save(args.output)

    print(save_path)


if __name__ == "__main__":
    main()
