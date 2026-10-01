import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime

from .implied_vol import implied_vol

def fetch_chain(ticker, min_days = 25):
    tk = yf.Ticker(ticker)
    spot = float(tk.history(period = "1d")["Close"].iloc[-1])
    today = datetime.now().date()

    expiry = None
    for d in tk.options:
        dte = (datetime.strptime(d, "%Y-%m-%d").date() - today).days
        if dte >= min_days:
            expiry = d
            break
    
    if expiry is None:
        raise ValueError(f"No expiration at least {min_days} days out")
    
    dte = (datetime.strptime(expiry, "%Y-%m-%d").date() - today).days
    T = dte / 365.0
        
    chain = tk.option_chain(expiry)
    return spot, expiry, T, chain.calls, chain.puts

def clean_chain(calls, spot, moneyness = 0.15):
    df = calls.copy()

    df = df[(df["bid"] > 0) & (df["ask"] > 0)]
    df = df[(df["volume"].fillna(0) > 0) | (df["openInterest"].fillna(0) >0)]
    df = df[(df["strike"] > (1 - moneyness) * spot) & (df["strike"] < (1 + moneyness) * spot)]

    df["mid"] = (df["bid"] + df["ask"]) / 2
    df = df[(df["ask"] - df["bid"]) / df["mid"] < 0.5]

    return df.reset_index(drop = True)

def compute_smile(df, spot, T, r = 0.04, q = 0.0, option_type = "call"):
        strikes, ivs = [], []

        for _, row in df.iterrows():
            try:
                iv = implied_vol(row["mid"], spot, row["strike"], T, r, q=q, option_type=option_type)
            except (ValueError, ZeroDivisionError, OverflowError):
                continue

            if 0.01 < iv < 3.0:
                strikes.append(row["strike"])
                ivs.append(iv)

        return np.array(strikes), np.array(ivs)

def implied_spot(calls, puts, spot, T, r=0.04):
    c = calls[["strike", "bid", "ask"]]
    p = puts[["strike", "bid", "ask"]]
    m = c.merge(p, on="strike", suffixes=("_c", "_p"))

    m = m[(m["bid_c"] > 0) & (m["bid_p"] > 0)]
    m = m[(m["strike"] > 0.98 * spot) & (m["strike"] < 1.02 * spot)]

    mid_c = (m["bid_c"] + m["ask_c"]) / 2
    mid_p = (m["bid_p"] + m["ask_p"]) / 2
    s_eff = mid_c - mid_p + m["strike"] * np.exp(-r * T)

    return float(s_eff.median())