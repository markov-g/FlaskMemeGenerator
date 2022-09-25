from ingestor_interface import IngestorInterface
from quote_model import QuoteModel
from typing import List
import docx
from pathlib import Path

class MSWordIngestor(IngestorInterface):
    supported_file_ext = [ ".doc", ".docx" ]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        assert cls.can_ingest(path)
        file_location: Path = Path(path)

        extracted_quotes = []

        # http://theautomatic.net/2019/10/14/how-to-read-word-documents-with-python/
        doc = docx.Document(file_location)
        for p in doc.paragraphs:
            if p.text != '':
                parsed = p.text.split(' - ')
                quote = QuoteModel(parsed[0], parsed[1])
                extracted_quotes.append(quote)

        return extracted_quotes

