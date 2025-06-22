import regex as re
from typing import List, Dict, Any
from src.validation.Validator import Validator
from src.utils.Constants import *


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
                    if direction == CREDIT:  # Money out
                        calculated_balance -= amount
                    elif direction == DEBIT:  # Money in
                        calculated_balance += amount

                discrepancy = abs(calculated_balance - end_balance)
                result[bank_name] = discrepancy <= 10.0

            except (KeyError, TypeError, ValueError):
                result[bank_name] = False
        self.validation_result = result
        return self.validation_result

    def get_discrepancy(self) -> Dict[str, str]:
        result = {}
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

                result[bank_name] = (
                    f"Calculated ending balance: {calculated_balance:.2f}\n"
                    f"Provided ending balance: {end_balance:.2f}\n"
                    f"Discrepancy: {discrepancy:+.2f}\n"
                    f"Total Credit: {total_credit:.2f}\n"
                    f"Total Debit: {total_debit:.2f}\n"
                    f"Discrepancy as % of transaction volume: {discrepancy_percent}"
                )

            except Exception as e:
                result[bank_name] = f"Error calculating discrepancy: {str(e)}"
        self.discrepancy = result
        return self.discrepancy
