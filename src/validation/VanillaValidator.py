import regex as re
from typing import List, Dict, Any
from src.validation.Validator import Validator
from src.utils.Constants import *


class VanillaValidator(Validator):

    def __init__(self, data: Dict):
        if data is None:
            raise Exception("Data is null for validation")
        self.data = data

    def validate(self) -> bool:

        try:
            data = self.data
            start_balance = data[STARTING_BALANCE]
            end_balance = data[ENDING_BALANCE]
            transactions = data[TRANSACTIONS]

            calculated_balance = start_balance

            for txn in transactions:
                amount = txn[AMOUNT]
                direction = txn[DIRECTION].lower()
                if direction == CREDIT:  # Money out
                    calculated_balance -= amount
                elif direction == DEBIT:  # Money in
                    calculated_balance += amount

            discrepancy = abs(calculated_balance - end_balance)
            return discrepancy <= 10.0

        except (KeyError, TypeError, ValueError) as e:
            return False

    def get_discrepancy(self) -> str:

        try:
            start_balance = self.data[STARTING_BALANCE]
            end_balance = self.data[ENDING_BALANCE]
            transactions = self.data[TRANSACTIONS]

            calculated_balance = start_balance

            for txn in transactions:
                amount = txn[AMOUNT]
                direction = txn[DIRECTION].lower()
                if direction == CREDIT:
                    calculated_balance -= amount
                elif direction == DEBIT:
                    calculated_balance += amount

            discrepancy = round(calculated_balance - end_balance, 2)

            return (
                f"Calculated ending balance: {calculated_balance:.2f}\n"
                f"Provided ending balance: {end_balance:.2f}\n"
                f"Discrepancy: {discrepancy:+.2f}"
            )
        except Exception as e:
            return f"Error calculating discrepancy: {str(e)}"
