from typing import List
from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel
from .pdf_ingestor import PDFIngestor
from .msword_ingestor import MSWordIngestor
from .csv_ingestor import CSVIngestor
from .txt_ingestor import TXTIngestor

class Ingestor(IngestorInterface):
    ingestors: List[IngestorInterface] = [
        PDFIngestor,
        MSWordIngestor,
        CSVIngestor,
        TXTIngestor,
    ]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        for ingestor in cls.ingestors:
            print(f"Testing ingestor: {ingestor}")
            if ingestor.can_ingest(path=path):
                print(f"Match: {ingestor}")
                return ingestor.parse(path)
        else:
            print("No suitable ingestor found!")

if __name__ == '__main__':
    model: List[QuoteModel] = Ingestor.parse(path="/Users/r1pp3r/git-repos/github.com/PythonPlayground/Udacity_Python/MemeGenerator/_data/SimpleLines/SimpleLines.docx")
    if model != None:
        for m in model:
            print(f"Quote: {m.body}, by author:  {m.author}")
