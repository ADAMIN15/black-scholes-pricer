import pytest

from src.bs_pricer.greeks import delta, gamma, vega, theta, rho

S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2


def test_delta_call_known_value():
    assert delta(S, K, T, r, sigma) == pytest.approx(0.636831, abs=1e-5)


def test_gamma_known_value():
    assert gamma(S, K, T, r, sigma) == pytest.approx(0.018762, abs=1e-5)


def test_vega_known_value():
    assert vega(S, K, T, r, sigma) == pytest.approx(37.524035, abs=1e-5)


def test_rho_call_known_value():
    assert rho(S, K, T, r, sigma) == pytest.approx(53.232482, abs=1e-5)


def test_theta_call_is_negative():
    assert theta(S, K, T, r, sigma) == pytest.approx(-6.414, abs=1e-2)


def test_delta_relationship():
    d_call = delta(S, K, T, r, sigma, option_type="call")
    d_put = delta(S, K, T, r, sigma, option_type="put")
    assert d_call - d_put == pytest.approx(1.0, abs=1e-12)


def test_gamma_and_vega_are_positive():
    assert gamma(S, K, T, r, sigma) > 0
    assert vega(S, K, T, r, sigma) > 0


def test_rho_put_is_negative():
    assert rho(S, K, T, r, sigma, option_type="put") < 0