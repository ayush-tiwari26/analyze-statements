import regex as re
from typing import List, Dict, Any
from src.extraction.Extractor import Extractor
from src.parsers.Parser import Parser


class VanillaExtractor(Extractor):

    # --- REGEX PATTERNS ---
    COLUMNAR_PATTERN = re.compile(
        r"^(?P<date>\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\s+"  # 1. Date (e.g., 01/15/2024)
        r"(?P<description>.+?)\s{2,}"  # 2. Description (non-greedy, followed by at least 2 spaces)
        r"(?P<debit>[\d,]+\.\d{2})?\s+"  # 3. Debit amount (optional)
        r"(?P<credit>[\d,]+\.\d{2})?\s+"  # 4. Credit amount (optional)
        r"([\d,]+\.\d{2})$"  # 5. Ending balance (must be present to anchor the line)
    )
    INLINE_PATTERN = re.compile(
        r"^(?P<date>\d{1,2}[-/]\d{1,2}[/-]\d{2,4})\s+"  # 1. Date
        r"(?P<description>.+?)\s+"  # 2. Description (non-greedy)
        r"(?P<amount>[\d,]+\.\d{2})\s+"  # 3. Amount
        r"(?P<direction>Debit|Credit|DR|CR)\b",  # 4. Direction (as a whole word, case-insensitive)
        re.IGNORECASE
    )

    def __init__(self, parser):
        self.data: Dict = None
        self.parser: Parser = parser

    def extract(self) -> Dict[str, Dict]:
        self.data = self.parser.get_content()
        extracted_data = {}
        for key in self.data.keys():
            extracted_data[key] = self.extract_single(self.data[key])
        return extracted_data

    def extract_single(self, content: str) -> Dict:
        """
        Parses a raw string from a bank statement to extract a structured list of transactions.
        """
        transactions: List[Dict[str, Any]] = []

        def _parse_amount(amount_str: str) -> float:
            if not amount_str:
                return 0.0
            return float(amount_str.replace(',', ''))

        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue

            match = self.COLUMNAR_PATTERN.search(line)
            if match:
                data = match.groupdict()
                transaction_info = {
                    'date': data['date'],
                    'description': data['description'].strip()
                }

                debit_amount = _parse_amount(data.get('debit'))
                credit_amount = _parse_amount(data.get('credit'))

                if debit_amount > 0:
                    transactions.append({**transaction_info, 'amount': debit_amount, 'direction': 'Debit'})
                    continue

                if credit_amount > 0:
                    transactions.append({**transaction_info, 'amount': credit_amount, 'direction': 'Credit'})
                    continue

            match = self.INLINE_PATTERN.search(line)
            if match:
                data = match.groupdict()
                transaction = {
                    'date': data['date'],
                    'description': data['description'].strip(),
                    'amount': _parse_amount(data['amount']),
                    'direction': data['direction'].capitalize()  # Standardize to "Debit" or "Credit"
                }
                transactions.append(transaction)

        return {'transactions': transactions}
