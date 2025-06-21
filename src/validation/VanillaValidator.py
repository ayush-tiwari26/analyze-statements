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
            start_balance = self.data[STARTING_BALANCE]
            end_balance = self.data[ENDING_BALANCE]
            transactions = self.data[TRANSACTIONS]

            calculated_balance = start_balance

            for txn in transactions:
                amount = abs(txn[AMOUNT])
                direction = txn[DIRECTION].lower()
                if direction == CREDIT:  # Money out
                    calculated_balance -= amount
                elif direction == DEBIT:  # Money in
                    calculated_balance += amount

            discrepancy = abs(calculated_balance - end_balance)
            return discrepancy <= 10.0

        except (KeyError, TypeError, ValueError):
            return False

    def get_discrepancy(self) -> str:
        try:
            start_balance = self.data[STARTING_BALANCE]
            end_balance = self.data[ENDING_BALANCE]
            transactions = self.data[TRANSACTIONS]

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

            return (
                f"Calculated ending balance: {calculated_balance:.2f}\n"
                f"Provided ending balance: {end_balance:.2f}\n"
                f"Discrepancy: {discrepancy:+.2f}\n"
                f"Total Credit: {total_credit:.2f}\n"
                f"Total Debit: {total_debit:.2f}\n"
                f"Discrepancy as % of transaction volume: {discrepancy_percent}"
            )

        except Exception as e:
            return f"Error calculating discrepancy: {str(e)}"
