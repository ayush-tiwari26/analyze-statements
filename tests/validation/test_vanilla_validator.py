# tests/test_vanilla_validator.py
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

@pytest.fixture(autouse=True)
def _disable_io(monkeypatch, tmp_path):
    monkeypatch.setattr(
        "src.validation.VanillaValidator.VanillaValidator._save_discrepancy_to_excel",
        lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        "src.utils.load_configs.load_configs",
        lambda: {"validation_output_dir": tmp_path.as_posix()},
    )


BANK_DATA_VALID = {
    "BankA": {
        STARTING_BALANCE: 1_000.0,
        ENDING_BALANCE: 1_300.0,
        TRANSACTIONS: [
            {AMOUNT: 200.0, DIRECTION: DEBIT},
            {AMOUNT: 100.0, DIRECTION: DEBIT},
        ],
    },
    "BankB": {
        STARTING_BALANCE: 500.0,
        ENDING_BALANCE: 400.0,
        TRANSACTIONS: [
            {AMOUNT: 100.0, DIRECTION: CREDIT},
        ],
    },
}

BANK_DATA_INVALID = {
    "BankA": {
        STARTING_BALANCE: 1_000.0,
        ENDING_BALANCE: 1_350.0,                       # 50 off
        TRANSACTIONS: [
            {AMOUNT: 200.0, DIRECTION: DEBIT},
            {AMOUNT: 100.0, DIRECTION: DEBIT},
        ],
    },
    "BankB": {
        STARTING_BALANCE: 500.0,
        ENDING_BALANCE: 600.0,                         # 200 off
        TRANSACTIONS: [
            {AMOUNT: 100.0, DIRECTION: CREDIT},
        ],
    },
}

BANK_DATA_TOLERANCE = {
    "BankA": {
        STARTING_BALANCE: 1_000.0,
        ENDING_BALANCE: 1_208.5,                       # 8.5 off
        TRANSACTIONS: [
            {AMOUNT: 200.0, DIRECTION: DEBIT},
        ],
    },
}

def test_validate_success():
    result = VanillaValidator(BANK_DATA_VALID).validate()
    assert result == {"BankA": True, "BankB": True}


def test_validate_failure():
    result = VanillaValidator(BANK_DATA_INVALID).validate()
    assert result == {"BankA": False, "BankB": False}


def test_validate_within_tolerance():
    res = VanillaValidator(BANK_DATA_TOLERANCE).validate()
    assert res == {"BankA": True}


def test_get_discrepancy_human_readable():
    validator = VanillaValidator(BANK_DATA_VALID)
    output = validator.get_discrepancy()

    assert set(output.keys()) == {"BankA", "BankB"}

    txt = output["BankA"]
    assert "Calculated ending balance:" in txt
    assert "Provided ending balance:" in txt
    assert "Discrepancy:" in txt
    assert "Total Credit:" in txt
    assert "Total Debit:" in txt
    assert "Discrepancy as % of transaction volume:" in txt
