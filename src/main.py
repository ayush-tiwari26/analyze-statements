import json
from src.extraction.LLMExtractor import LLMExtractor
from src.extraction.VanillaExtractor import VanillaExtractor
from src.parsers.PdfParser import PdfParser
from src.utils.LLMRouter import LLMRouter, Model
from src.utils.load_configs import load_configs
from src.validation.VanillaValidator import VanillaValidator
from src.visualization.Visualizer import Visualizer

if __name__ == '__main__':
    config = load_configs()
    # Loading data
    parser = PdfParser(config=config)
    # Extracting data
    extractor = LLMExtractor(parser)
    data = extractor.parse_data()
    for name in data.keys():
        if name == '18.pdf':
            test_content = data[name]
    # Sample for 1 Bank
    statement = extractor.extract_data(test_content)
    print(json.dumps(statement))

    # Validation
    validator = VanillaValidator(statement)
    print(validator.validate())
    print(validator.get_discrepancy())

    # Visualization
    visualizer = Visualizer()
    visualizer.plot_balance_distribution(statement)
    visualizer.save_plot(config)
