import pymupdf  # Also known as fitz
from typing import List, Dict, Any
from pathlib import Path
from src.parsers.Parser import Parser


class PdfParser(Parser):
    """
    A parser to find all PDF files within a specified local directory
    and extract their text content into a dictionary.
    """

    def __init__(self, config: Dict[str, Any]):
        source_path_str = config.get("local_pdf_source")
        if not source_path_str:
            raise ValueError("Configuration object must contain a 'local_pdf_source' key.")

        self.source_directory = Path(source_path_str)
        # Internal state to hold the list of discovered file paths
        self.pdf_files: List[Path] = []

    def get_files(self) -> List[Path]:
        print(f"Scanning for PDF files in: '{self.source_directory}'")

        if not self.source_directory.is_dir():
            raise FileNotFoundError(f"The specified source directory does not exist: {self.source_directory}")

        self.pdf_files = list(self.source_directory.rglob("*.pdf"))

        print(f"Found {len(self.pdf_files)} PDF file(s).")
        return self.pdf_files

    def get_content(self) -> Dict[str, str]:
        if not self.pdf_files:
            self.get_files()

        all_content = {}
        for pdf_path in self.pdf_files:
            try:
                doc = pymupdf.open(pdf_path)
                full_text = ""
                for page in doc:
                    full_text += page.get_text("text")
                doc.close()
                # Use the filename as the key
                all_content[pdf_path.name] = full_text
            except Exception as e:
                error_message = f"Error reading file: {e}"
                print(f"Failed to process {pdf_path.name}. Reason: {e}")
                all_content[pdf_path.name] = error_message

        return all_content
