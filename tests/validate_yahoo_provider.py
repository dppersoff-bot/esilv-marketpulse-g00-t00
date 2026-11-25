"""Exercice TD08 : validation de fetch_prices_for_ticker().

Lancer depuis la racine du dépôt (yfinance doit être installé) :
    python tests/validate_yahoo_provider.py

Partie 1 : tests hors ligne (mapping, paramètres, ticker inconnu).
Partie 2 : vraie récupération Yahoo pour AAPL et SP500. Si Yahoo est
indisponible, le script l'indique (PENDING_EXTERNAL) sans inventer de données.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.providers import yahoo_provider
from src.providers.yahoo_provider import fetch_prices_for_ticker

# ---------- Partie 1 : tests hors ligne ----------
calls = []
original_fetch = yahoo_provider.fetch_yahoo_prices


def fake_fetch(symbol, canonical_ticker, period="1mo", interval="1d"):
    calls.append((symbol, canonical_ticker, period, interval))
    return []


yahoo_provider.fetch_yahoo_prices = fake_fetch
try:
    fetch_prices_for_ticker("AAPL")
    fetch_prices_for_ticker("SP500")
    fetch_prices_for_ticker("AAPL", period="3mo", interval="1d")
finally:
    yahoo_provider.fetch_yahoo_prices = original_fetch

assert calls[0] == ("AAPL", "AAPL", "1mo", "1d"), calls[0]
assert calls[1] == ("^GSPC", "SP500", "1mo", "1d"), calls[1]
assert calls[2] == ("AAPL", "AAPL", "3mo", "1d"), calls[2]
print("Mapping et transmission de period / interval : OK")

try:
    fetch_prices_for_ticker("UNKNOWN")
except ValueError as error:
    print(f"ValueError bien levée pour UNKNOWN : {error}")
else:
    raise AssertionError("fetch_prices_for_ticker('UNKNOWN') aurait dû lever ValueError")

print("Tests hors ligne réussis.\n")


# ---------- Partie 2 : vraie récupération Yahoo ----------
def check_types(rows, ticker):
    assert rows, f"Série {ticker} vide"
    for row in rows:
        assert isinstance(row["date"], str) and len(row["date"]) == 10
        assert row["ticker"] == ticker
        for key in ("open", "high", "low", "close"):
            assert isinstance(row[key], float)
        assert isinstance(row["volume"], int)


try:
    apple = fetch_prices_for_ticker("AAPL")
    sp500 = fetch_prices_for_ticker("SP500")
    apple_3_months = fetch_prices_for_ticker("AAPL", period="3mo", interval="1d")
except Exception as error:  # réseau coupé, Yahoo bloqué, etc.
    print(f"PENDING_EXTERNAL : récupération Yahoo impossible ({type(error).__name__}: {error})")
else:
    check_types(apple, "AAPL")
    check_types(sp500, "SP500")
    check_types(apple_3_months, "AAPL")
    assert len(apple_3_months) > len(apple)
    print(f"AAPL  (1mo) : {len(apple)} observations, {apple[0]['date']} -> {apple[-1]['date']}")
    print(f"SP500 (1mo) : {len(sp500)} observations, {sp500[0]['date']} -> {sp500[-1]['date']}")
    print(f"AAPL  (3mo) : {len(apple_3_months)} observations")
    print(f"Dernier close AAPL : {apple[-1]['close']:.2f} | SP500 : {sp500[-1]['close']:.2f}")
    print("Récupération Yahoo réelle réussie.")
