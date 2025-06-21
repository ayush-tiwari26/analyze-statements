import pymupdf
from typing import List, Dict, Any
from pathlib import Path
from src.parsers.Parser import Parser


class PdfParser(Parser):
    """
    A parser to find all PDF files within a specified local directory
    and extract their text content.
    """

    def __init__(self, config: Dict[str, Any]):
        source_path_str = config.get("local_pdf_source")
        if not source_path_str:
            raise ValueError("Configuration object must contain a 'local_pdf_source' key.")

        self.source_directory = Path(source_path_str)
        self.pdf_files: List[Path] = []

    def get_files(self) -> List[Path]:
        print(f"Scanning for PDF files in: '{self.source_directory}'")

        if not self.source_directory.is_dir():
            raise FileNotFoundError(f"The specified source directory does not exist: {self.source_directory}")

        self.pdf_files = list(self.source_directory.rglob("*.pdf"))

        print(f"Found {len(self.pdf_files)} PDF file(s).")
        return self.pdf_files

    def get_content(self, pdf_path: Path) -> str:
        print(f"Extracting content from: {pdf_path.name}")
        try:
            doc = pymupdf.open(pdf_path)
            full_text = ""
            for page in doc:
                full_text += page.get_text()
            doc.close()
            return full_text
        except Exception as e:
            print(f"Error reading PDF file {pdf_path}: {e}")
            return ""
