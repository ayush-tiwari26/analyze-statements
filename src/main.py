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
    extractor = LLMExtractor(parser, Model.LLAMA_SM)
    bank_statements = extractor.extract()
    print(json.dumps(bank_statements))

    # Validation
    validator = VanillaValidator(bank_statements)
    is_valid = validator.validate()
    discrepancies = validator.get_discrepancy()

    for name in is_valid.keys():
        print(f"Validating for Bank: {name}")
        if not is_valid[name]:
            print(f"\tStatement is Invalid")
            print(f"\t{validator.get_discrepancy()}")
        else:
            print(f"\tStatement is valid")
        print("=======================================\n\n")

    # Visualization
    visualizer = Visualizer()
    visualizer.plot_balance_distribution(bank_statements)
    visualizer.save_plot(config)
