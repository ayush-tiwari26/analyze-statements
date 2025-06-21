from src.extraction.LLMExtractor import LLMExtractor
from src.extraction.VanillaExtractor import VanillaExtractor
from src.parsers.PdfParser import PdfParser
from src.utils.LLMRouter import LLMRouter, Model
from src.utils.load_configs import load_configs
from src.validation.VanillaValidator import VanillaValidator

if __name__ == '__main__':
    config = load_configs()
    parser = PdfParser(config=config)
    files = parser.get_files()
    extractor = VanillaExtractor(parser)
    data = extractor.parse_data()
    for name in data.keys():
        if name == '18.pdf':
            test_content = data[name]

    extractor = LLMExtractor(parser)
    json_data = extractor.extract_data(test_content)
    validator = VanillaValidator(json_data)
    print(validator.validate())
    print(validator.get_discrepancy())

