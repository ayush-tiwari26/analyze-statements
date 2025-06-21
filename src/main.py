from src.parsers.PdfParser import PdfParser
from src.utils.load_configs import load_configs

if __name__ == '__main__':
    config = load_configs()
    parser = PdfParser(config=config)
    files = parser.get_files()
    print(f"\nInstance state check: {len(parser.downloaded_files)} files stored in parser object.")
    if files:
        first_file_path = files[0]
        content = parser.get_content(first_file_path)
        print(f"\n--- Content of {first_file_path.name} (first 500 characters) ---")
        print(content[:500])
        print("...")
