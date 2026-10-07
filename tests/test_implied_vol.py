import pytest

from src.bs_pricer.pricing import bs_price
from src.bs_pricer.implied_vol import implied_vol


def test_recovers_known_call_vol():
    price = bs_price(100, 100, 1, 0.05, 0.2)
    assert implied_vol(price, 100, 100, 1, 0.05) == pytest.approx(0.2, abs=1e-4)


def test_recovers_known_put_vol():
    price = bs_price(100, 110, 0.5, 0.03, 0.35, option_type="put")
    solved = implied_vol(price, 100, 110, 0.5, 0.03, option_type="put")
    assert solved == pytest.approx(0.35, abs=1e-4)


def test_round_trip_across_strikes():
    for strike in [80, 90, 100, 110, 120]:
        price = bs_price(100, strike, 1, 0.05, 0.25)
        assert implied_vol(price, 100, strike, 1, 0.05) == pytest.approx(0.25, abs=1e-4)


def test_raises_when_no_solution_exists():
    with pytest.raises(ValueError):
        implied_vol(0.0001, 100, 50, 1, 0.05)