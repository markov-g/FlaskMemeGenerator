from ingestor_interface import IngestorInterface
from quote_model import QuoteModel
from typing import List
from pathlib import Path
import csv

class CSVIngestor(IngestorInterface):
    supported_file_ext = [ ".csv" ]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        assert cls.can_ingest(path)
        file_location: Path = Path(path)

        extracted_quotes = []

        with open(file_location, 'r', encoding="utf-8") as file_in:
            csv_reader = csv.DictReader(file_in)
            for row in csv_reader:
                quote = QuoteModel(row['body'], row['author'])
                extracted_quotes.append(quote)

        return extracted_quotes
