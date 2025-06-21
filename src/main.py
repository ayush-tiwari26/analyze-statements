from src.extraction.VanillaExtractor import VanillaExtractor
from src.parsers.Pdf2MarkdownParser import Pdf2MarkdownParser
from src.parsers.PdfParser import PdfParser
from src.utils.load_configs import load_configs

if __name__ == '__main__':
    config = load_configs()
    parser = Pdf2MarkdownParser(config=config)
    files = parser.get_files()
    extractor = VanillaExtractor(parser)
    data = extractor.parse_data()
    print(list(data)[0])
    statement = extractor.extract_data(list(data)[0])
    statement = extractor.extract_data(list(data)[2])
    statement = extractor.extract_data(list(data)[4])
    print(statement)
