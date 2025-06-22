from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
from typing import List, Dict
from pathlib import Path
from src.parsers.Parser import Parser
from src.utils.disk_cache import get_disk_cache, set_disk_cache
from src.utils.load_configs import load_configs


class Pdf2MarkdownParser(Parser):
    """
    A parser that uses the 'marker' library to convert PDFs to Markdown.
    """

    def __init__(self):
        source_path_str = load_configs().get("local_pdf_source")
        if not source_path_str:
            raise ValueError("Configuration must contain 'local_pdf_source'.")

        self.source_directory = Path(source_path_str)
        self.pdf_files: List[Path] = []

        # Initialize PdfConverter with model artifacts
        print("Loading Marker models... This may take a moment.")
        self.converter = PdfConverter(
            artifact_dict=create_model_dict()
        )
        print("Marker models loaded successfully.")

    def get_files(self) -> List[Path]:
        print(f"Scanning for PDF files in: '{self.source_directory}'")

        if not self.source_directory.is_dir():
            raise FileNotFoundError(f"Directory does not exist: {self.source_directory}")

        self.pdf_files = list(self.source_directory.rglob("*.pdf"))
        print(f"Found {len(self.pdf_files)} PDF file(s).")
        return self.pdf_files

    def get_content(self) -> Dict[str, str]:
        if not self.pdf_files:
            self.get_files()

        all_markdown_content = {}

        for pdf_path in self.pdf_files:
            # Disk persistent caching of python objects for efficiency
            print(f"Converting to Markdown: {pdf_path.name}")
            try:
                cached_markdown_text = get_disk_cache(pdf_path.name)
                if cached_markdown_text is not None:
                    all_markdown_content[pdf_path.name] = cached_markdown_text
                else:
                    rendered = self.converter(str(pdf_path))
                    markdown_text, _, _ = text_from_rendered(rendered)
                    all_markdown_content[pdf_path.name] = markdown_text
                    try:
                        set_disk_cache(pdf_path.name, markdown_text)
                    except Exception as e:
                        print(f"Failed to cache content for {pdf_path.name}")
            except Exception as e:
                print(f"Failed to process {pdf_path.name}. Reason: {e}")
                all_markdown_content[pdf_path.name] = f"Error converting file: {e}"

        return all_markdown_content
