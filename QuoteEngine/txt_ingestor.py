from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel
from typing import List
from pathlib import Path

class TXTIngestor(IngestorInterface):
    supported_file_ext = [ ".txt" ]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        assert cls.can_ingest(path)
        file_location: Path = Path(path)

        extracted_quotes = []

        with open(file_location, 'r', encoding="utf-8") as file_in:
            for line in file_in.readlines():
                if len(line) > 0:
                    parsed = [quote_part.strip() for quote_part in line.split(' - ')]
                    if len(parsed) > 1:
                        quote = QuoteModel(parsed[0], parsed[1])
                        extracted_quotes.append(quote)

        return extracted_quotes