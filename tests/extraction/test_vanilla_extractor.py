import pytest
from tests.conftest import DummyParser
from src.extraction.VanillaExtractor import VanillaExtractor


def make_extractor(raw_pages: dict):
    """Utility: build a VanillaExtractor wired to our DummyParser."""
    return VanillaExtractor(parser=DummyParser(raw_pages))


# Columnar-layout tests
def test_columnar_extraction():
    raw = (
        "01/15/2024  Coffee Shop        5.50   0.00   950.00\n"
        "02/01/2024  Salary             0.00   1,500.00 2,450.00\n"
    )
    ext = make_extractor({"page1": raw})
    result = ext.extract_single(raw)["transactions"]

    # we expect two transactions
    assert len(result) == 2

    coffee, salary = result
    assert coffee == {
        "date": "01/15/2024",
        "description": "Coffee Shop",
        "amount": 5.50,
        "direction": "Debit",
    }
    assert salary["direction"] == "Credit"
    assert salary["amount"] == 1500.00


# Inline-layout tests
def test_inline_extraction():
    raw = (
        "03/10/2024 Grocery Store 123.45 Debit\n"
        "03/12/2024 Refund 99.99 Credit\n"
    )
    ext = make_extractor({"only_page": raw})
    txns = ext.extract_single(raw)["transactions"]

    assert [t["direction"] for t in txns] == ["Debit", "Credit"]
    assert txns[1]["amount"] == 99.99


# end-to-end extract()  (multi-page)
def test_extract_multiple_pages():
    data = {
        "page1": "04/01/2024 Lunch 25.00 Debit",
        "page2": "05/01/2024 Salary 2,500.00 Credit",
    }
    extractor = make_extractor(data)
    all_pages = extractor.extract()

    assert set(all_pages.keys()) == {"page1", "page2"}
    assert all_pages["page2"]["transactions"][0]["direction"] == "Credit"


# edge cases
@pytest.mark.parametrize("raw", ["", "This does not match anything"])
def test_no_transactions_found(raw):
    ext = make_extractor({"page": raw})
    assert ext.extract_single(raw)["transactions"] == []
