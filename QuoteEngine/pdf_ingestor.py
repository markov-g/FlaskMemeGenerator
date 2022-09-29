from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel
from pathlib import Path
from typing import List
import subprocess
import tempfile
from random import randint


class PDFIngestor(IngestorInterface):
    supported_file_ext = [ '.pdf' ]

    pdftotext_executable = '/Users/r1pp3r/PACKAGEMGMT/Homebrew/bin/pdftotext'

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        assert cls.can_ingest(path)

        extracted_quotes = []

        file_location: Path = Path(path)
        target_file = Path(tempfile.gettempdir(), f"pdf_to_text_{randint(0, 999999)}.txt")

        xpdf_parse_cmd = f"{cls.pdftotext_executable} -layout {file_location} {target_file}"  # see https://stackoverflow.com/questions/23089528/extracting-text-from-a-pdf-with-pdftotext

        try:
            subprocess.call(xpdf_parse_cmd, shell=True)
        except subprocess.CalledProcessError as error:
            print(f"Something went wrong trying to convert the PDF file at: {file_location} to text: {error}")

        try:
            with open(target_file, 'r') as txt_f:
                for line in txt_f.readlines():
                    if len(line) > 0:
                        parsed = [quote_part.strip() for quote_part in line.split(' - ')]
                        if len(parsed) > 1:
                            quote = QuoteModel(parsed[0], parsed[1])
                            extracted_quotes.append(quote)
        finally:
            pass
            # target_file.unlink()

        return extracted_quotes
