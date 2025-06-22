import logging

import pandas as pd
import os
from typing import Dict, Any

from src.utils.load_configs import load_configs
from src.validation.Validator import Validator
from src.utils.constants import *

class VanillaValidator(Validator):

    def __init__(self, data: Dict):
        if data is None:
            raise Exception("Data is null for validation")
        self.data = data
        self.validation_result = None
        self.discrepancy = None

    def validate(self) -> Dict[str, bool]:
        result = {}
        for bank_name in self.data.keys():
            try:
                start_balance = self.data[bank_name][STARTING_BALANCE]
                end_balance = self.data[bank_name][ENDING_BALANCE]
                transactions = self.data[bank_name][TRANSACTIONS]

                calculated_balance = start_balance

                for txn in transactions:
                    amount = abs(txn[AMOUNT])
                    direction = txn[DIRECTION].lower()
                    if direction == CREDIT:
                        calculated_balance -= amount
                    elif direction == DEBIT:
                        calculated_balance += amount

                discrepancy = abs(calculated_balance - end_balance)
                result[bank_name] = discrepancy <= VALIDATION_TOLERANCE

            except (KeyError, TypeError, ValueError):
                result[bank_name] = False
        self.validation_result = result
        return self.validation_result

    def get_discrepancy(self) -> Dict[str, str]:
        result = {}
        raw_result = {}
        for bank_name in self.data:
            try:
                start_balance = self.data[bank_name][STARTING_BALANCE]
                end_balance = self.data[bank_name][ENDING_BALANCE]
                transactions = self.data[bank_name][TRANSACTIONS]

                calculated_balance = start_balance
                total_credit = 0.0
                total_debit = 0.0

                for txn in transactions:
                    amount = abs(txn[AMOUNT])
                    direction = txn[DIRECTION].lower()
                    if direction == CREDIT:
                        total_credit += amount
                        calculated_balance -= amount
                    elif direction == DEBIT:
                        total_debit += amount
                        calculated_balance += amount

                discrepancy = round(calculated_balance - end_balance, 2)
                transaction_volume = total_credit + total_debit

                if transaction_volume == 0:
                    discrepancy_percent = "N/A"
                else:
                    discrepancy_percent = f"{(abs(discrepancy) / transaction_volume) * 100:.2f}%"

                raw_result[bank_name] = {
                    CSV_CALC_ENDING_BALANCE: calculated_balance,
                    CSV_INIT_ENDING_BALANCE: end_balance,
                    CSV_DISCREPANCY: discrepancy,
                    CSV_TOTAL_CREDIT: total_credit,
                    CSV_TOTAL_DEBIT: total_debit,
                    CSV_DISCREPANCY_PERCENTAGE: discrepancy_percent
                }

                result[bank_name] = (
                    f"Calculated ending balance: {calculated_balance:.2f}\n"
                    f"Provided ending balance: {end_balance:.2f}\n"
                    f"Discrepancy: {discrepancy:+.2f}\n"
                    f"Total Credit: {total_credit:.2f}\n"
                    f"Total Debit: {total_debit:.2f}\n"
                    f"Discrepancy as % of transaction volume: {discrepancy_percent}"
                )

            except Exception as e:
                raw_result[bank_name] = None
                result[bank_name] = f"Error calculating discrepancy: {str(e)}"

        self.discrepancy = result
        self._save_discrepancy_to_excel(raw_result)
        return self.discrepancy

    def _save_discrepancy_to_excel(self, discrepancy_data: Dict[str, Dict]):
        rows = []
        for bank_name, details in discrepancy_data.items():
            if details is None:
                row = [bank_name] + [""] * 6
            else:
                row = [bank_name]
                for key, value in details.items():
                    row.append(value)
            rows.append(row)

        columns = [
            "Bank Name",
            "Calculated ending balance",
            "Provided ending balance",
            "Discrepancy",
            "Total Credit",
            "Total Debit",
            "Discrepancy as % of transaction volume"
        ]
        df = pd.DataFrame(rows, columns=columns)

        output_dir = load_configs()["validation_output_dir"]
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "validation_results.xlsx")
        df.to_excel(output_path, index=False)
