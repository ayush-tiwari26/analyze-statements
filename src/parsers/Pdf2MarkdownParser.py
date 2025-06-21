# First, ensure you have marker-pdf and its dependencies installed:
# pip install marker-pdf torch

from marker.convert import convert_single_pdf
from marker.models import load_all_models
from typing import List, Dict, Any
from pathlib import Path

from src.parsers.Parser import Parser


class Pdf2MarkdownParser(Parser):
    """
    A parser that utilizes the 'marker-pdf' library to convert all PDF files
    within a specified local directory into Markdown format.
    """
    def __init__(self, config: Dict[str, Any]):
        source_path_str = config.get("local_pdf_source")
        if not source_path_str:
            raise ValueError("Configuration object must contain a 'local_pdf_source' key.")

        self.source_directory = Path(source_path_str)
        self.pdf_files: List[Path] = []

        # Load the models once during initialization for efficiency
        print("Loading Marker models... This may take a moment.")
        self.marker_models = load_all_models()
        print("Marker models loaded successfully.")

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

        all_markdown_content = {}
        for pdf_path in self.pdf_files:
            print(f"Converting to Markdown: {pdf_path.name}")
            try:
                # Use the convert_single_pdf function from the marker library
                markdown_text, _, _ = convert_single_pdf(str(pdf_path), self.marker_models)

                # Use the filename as the key
                all_markdown_content[pdf_path.name] = markdown_text
            except Exception as e:
                error_message = f"Error converting file with Marker: {e}"
                print(f"Failed to process {pdf_path.name}. Reason: {e}")
                all_markdown_content[pdf_path.name] = error_message

        return all_markdown_content
