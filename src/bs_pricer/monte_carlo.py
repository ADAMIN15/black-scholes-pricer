import numpy as np

def mc_price(S, K, T, r, sigma, q = 0.0, option_type = "call", n_sims = 100000, seed = None):
    if seed is not None:
        np.random.seed(seed)

    Z = np.random.standard_normal(n_sims)
    S_T = S * np.exp((r - q - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    if option_type == "call":
        payoffs = np.maximum(S_T - K, 0)
    elif option_type == "put":
        payoffs = np.maximum(K - S_T, 0)
    else: 
        raise ValueError("option_type must be 'call' or 'put'")
    
    price = np.exp(-r * T) * np.mean(payoffs)
    return price