import numpy as np
import pytest

from src.bs_pricer.pricing import bs_price


def test_call_price_known_value():
    assert bs_price(100, 100, 1, 0.05, 0.2) == pytest.approx(10.450584, abs=1.e-5)

def test_put_price_known_value():
    assert bs_price(100,100,1,0.05,0.2,option_type="put") == pytest.approx(5.573526, abs=1.e-5)

def test_put_call_parity():
    S,K,T,r,sigma = 100,100,1,0.05,0.2
    c = bs_price(S, K, T, r, sigma, option_type="call")
    p = bs_price(S, K, T, r, sigma, option_type="put")
    assert c - p == pytest.approx(S-K * np.exp(-r*T), abs=1e-10)

def test_price_increases_with_volatility():
    low = bs_price(100,100,1,0.05,0.15)
    high = bs_price(100,100,1,0.05,0.30)
    assert high > low

def test_invalid_option_type_raises():
    with pytest.raises(ValueError):
        bs_price(100,100,1,0.05,0.2,option_type="banana")