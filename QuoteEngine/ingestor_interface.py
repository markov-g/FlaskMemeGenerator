import abc
from pathlib import Path
from typing import List
from quote_model import QuoteModel

class IngestorInterface:
    supported_file_ext: List[str] = []

    @classmethod
    @abc.abstractmethod
    def can_ingest(cls, path: str) -> bool:
        file_loc = Path(path)
        file_ext = file_loc.suffix
        return file_ext in cls.supported_file_ext

    @classmethod
    @abc.abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        pass
