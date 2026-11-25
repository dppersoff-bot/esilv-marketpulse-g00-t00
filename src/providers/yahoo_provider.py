"""Fournisseur Yahoo Finance de MarketPulse (TD08).

Récupère des prix via yfinance et les convertit au format canonique :
{"date": str AAAA-MM-JJ, "ticker": str, "open": float, "high": float,
 "low": float, "close": float, "volume": int}

Aucune récupération n'est exécutée à l'import du module.
"""

import yfinance as yf

# Ticker interne MarketPulse -> symbole Yahoo Finance
YAHOO_SYMBOL_MAPPING = {
    "AAPL": "AAPL",
    "SP500": "^GSPC",
}


def fetch_yahoo_prices(symbol, canonical_ticker, period="1mo", interval="1d"):
    """Récupère l'historique Yahoo de `symbol` et le renvoie au format canonique.

    `canonical_ticker` est l'identifiant MarketPulse écrit dans chaque
    observation (ex. "SP500" même si Yahoo utilise "^GSPC").
    """
    history = yf.Ticker(symbol).history(
        period=period,
        interval=interval,
        auto_adjust=False,
    )

    if history.empty:
        raise ValueError(f"No Yahoo Finance data returned for symbol {symbol}.")

    rows = []
    for timestamp, row in history.iterrows():
        rows.append({
            "date": timestamp.strftime("%Y-%m-%d"),
            "ticker": canonical_ticker,
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": int(row["Volume"]),
        })
    return rows


def fetch_prices_for_ticker(ticker, period="1mo", interval="1d"):
    """Récupère les prix d'un ticker MarketPulse (ex. "AAPL", "SP500").

    Le symbole Yahoo est retrouvé automatiquement dans YAHOO_SYMBOL_MAPPING.
    Lève ValueError si le ticker n'est pas reconnu.
    """
    if ticker not in YAHOO_SYMBOL_MAPPING:
        supported = ", ".join(sorted(YAHOO_SYMBOL_MAPPING))
        raise ValueError(
            f"Unknown ticker '{ticker}'. Supported tickers: {supported}."
        )

    symbol = YAHOO_SYMBOL_MAPPING[ticker]
    return fetch_yahoo_prices(symbol, ticker, period=period, interval=interval)
