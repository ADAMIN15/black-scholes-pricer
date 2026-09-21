import numpy as np
from .pricing import bs_price
from .greeks import vega

def implied_vol(market_price, S, K, T, r, q = 0.0, option_type = "call", initial_guess = 0.2, tol = 1e-6, max_iter=100):
    sigma = initial_guess
    
    for i in range(max_iter):
        price = bs_price(S, K, T, r, sigma, q, option_type)
        diff = price - market_price

        if abs(diff) < tol:
            return sigma
        
        v = vega(S, K, T, r, sigma, q)
        sigma = sigma - diff / v

    raise ValueError("Implied volatility did not converge")