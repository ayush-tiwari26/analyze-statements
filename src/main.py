import json
from src.extraction.LLMExtractor import LLMExtractor
from src.parsers.Pdf2MarkdownParser import Pdf2MarkdownParser
from src.parsers.PdfParser import PdfParser
from src.utils.LLMRouter import LLMRouter, Model
from src.utils.load_configs import load_configs
from src.validation.VanillaValidator import VanillaValidator
from src.visualization.Visualizer import Visualizer

if __name__ == '__main__':
    config = load_configs()
    # Loading data
    parser = Pdf2MarkdownParser()
    # Extracting data
    extractor = LLMExtractor(parser, Model.LLAMA_LG)
    bank_statements = extractor.extract()
    print(json.dumps(bank_statements))

    # Validation
    validator = VanillaValidator(bank_statements)
    is_valid = validator.validate()
    discrepancies = validator.get_discrepancy()

    for name in is_valid.keys():
        print(f"Validating for Bank: {name}")
        if not is_valid[name]:
            print(f"! Statement has discrepancy")
            print(f"{validator.get_discrepancy()[name]}")
        else:
            print(f"\tStatement is valid, no discrepancy")
        print("=======================================\n\n")

    # Visualization
    visualizer = Visualizer()
    visualizer.plot_balance_distribution(bank_statements)
    visualizer.save_plot(config)
