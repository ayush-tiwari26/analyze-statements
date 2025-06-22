import pytest
from src.validation.VanillaValidator import VanillaValidator
from src.utils.constants import (
    STARTING_BALANCE,
    ENDING_BALANCE,
    TRANSACTIONS,
    AMOUNT,
    DIRECTION,
    CREDIT,
    DEBIT,
)

def test_validate_success():
    data = {
        STARTING_BALANCE: 1000.0,
        ENDING_BALANCE: 1300.0,
        TRANSACTIONS: [
            {AMOUNT: 200.0, DIRECTION: DEBIT},
            {AMOUNT: 100.0, DIRECTION: DEBIT},
        ],
    }
    assert VanillaValidator(data).validate() is True

def test_validate_failure():
    data = {
        STARTING_BALANCE: 1000.0,
        ENDING_BALANCE: 1350.0,
        TRANSACTIONS: [
            {AMOUNT: 200.0, DIRECTION: DEBIT},
            {AMOUNT: 100.0, DIRECTION: DEBIT},
        ],
    }
    assert VanillaValidator(data).validate() is False

def test_validate_tolerance():
    data = {
        STARTING_BALANCE: 1000.0,
        ENDING_BALANCE: 1208.5,
        TRANSACTIONS: [
            {AMOUNT: 200.0, DIRECTION: DEBIT},
        ],
    }
    assert VanillaValidator(data).validate() is True

def test_get_discrepancy_output():
    data = {
        STARTING_BALANCE: 1000.0,
        ENDING_BALANCE: 1300.0,
        TRANSACTIONS: [
            {AMOUNT: 200.0, DIRECTION: DEBIT},
            {AMOUNT: 100.0, DIRECTION: DEBIT},
        ],
    }
    output = VanillaValidator(data).get_discrepancy()
    assert "Calculated ending balance" in output
    assert "Provided ending balance" in output
    assert "Discrepancy:" in output
