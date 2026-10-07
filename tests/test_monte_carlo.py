import pytest

from src.bs_pricer.pricing import bs_price
from src.bs_pricer.monte_carlo import mc_price


def test_converges_to_closed_form_call():
    mc = mc_price(100, 100, 1, 0.05, 0.2, n_sims=200000, seed=42)
    bs = bs_price(100, 100, 1, 0.05, 0.2)
    assert mc == pytest.approx(bs, rel=0.01)


def test_converges_to_closed_form_put():
    mc = mc_price(100, 100, 1, 0.05, 0.2, option_type="put", n_sims=200000, seed=42)
    bs = bs_price(100, 100, 1, 0.05, 0.2, option_type="put")
    assert mc == pytest.approx(bs, rel=0.02)


def test_seed_makes_result_reproducible():
    a = mc_price(100, 100, 1, 0.05, 0.2, n_sims=10000, seed=7)
    b = mc_price(100, 100, 1, 0.05, 0.2, n_sims=10000, seed=7)
    assert a == b