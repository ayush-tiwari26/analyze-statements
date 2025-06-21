from typing import Dict

import json_repair

from src.extraction.Extractor import Extractor
from src.utils.LLMRouter import LLMRouter, Model


class LLMExtractor(Extractor):

    def __init__(self, parser, model=Model.LLAMA_LG):
        self.data = None
        self.parser = parser
        self.model = model

    def parse_data(self) -> Dict[str, str]:
        self.data = self.parser.get_content()
        return self.data

    def extract_data(self, content: str) -> Dict:
        router = LLMRouter()
        prompt = """
        
            Given the Raw text parsed from a pdf statement above.
            Give me the transactions as a structured reponse (in json format) to me
            
            Output must be:
            ■ JSON object 
            ■ Fields: 
                1. `starting_balance`: the starting balance of the statement
                2. `ending_balance`: the ending balance
                3. `transactions`: a list of json objects where each object has fields
                    3.1. `date`: The date of the transaction. MUST be in format YYYY-MM-DD
                    3.2 `description`: A brief description of the transaction. Preferably the name of receiver/sender.
                    3.3 `amount`: The monetary value of the transaction. MUST be positive.
                    3.4 `direction: Indicate whether the transaction is a `debit` or `credit` (always in small case).
                4. `discrepancy`: a one line string explaining any discrepancy if exists in this statement. (`null` if no discrepancy)
                
            NOTE: Do not include any commentary. Response must ONLY be a json
        """
        prompt = content + prompt
        json = router.hit(self.model, prompt)
        decoded_object = json_repair.loads(json)
        return decoded_object
