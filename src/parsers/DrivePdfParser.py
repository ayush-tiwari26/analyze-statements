import gdown
import pymupdf
from typing import List, Dict, Any
from pathlib import Path
from src.parsers.Parser import Parser


class DrivePdfParser(Parser):
    """
    A parser to download PDF files from a public Google Drive folder
    and extract their text content.
    """

    def __init__(self, config: Dict[str, Any]):
        self.drive_link: str = config.get("drive_input")
        if not self.drive_link:
            raise ValueError("Configuration object must contain a 'drive_input' key.")
        self.downloaded_files: List[Path] = []
        self.output_dir = Path("data/raw_pdfs")

    def get_files(self) -> List[Path]:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Attempting to download files from: {self.drive_link}")
        gdown.download_folder(self.drive_link, output=str(self.output_dir), quiet=True, use_cookies=False)
        self.downloaded_files = list(self.output_dir.rglob("*.pdf"))
        print(f"Successfully downloaded {len(self.downloaded_files)} PDF file(s).")
        return self.downloaded_files

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
