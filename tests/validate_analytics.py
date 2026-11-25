"""Exercice TD07 : validation du module src/analytics.py.

Lancer depuis la racine du dépôt :
    python tests/validate_analytics.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
    index_by_date,
)

# 1. Deux petites séries fictives (close en str, comme avec csv.DictReader)
instrument = [
    {"date": "2026-11-02", "ticker": "AAPL", "close": "100.0"},
    {"date": "2026-11-03", "ticker": "AAPL", "close": "104.0"},
    {"date": "2026-11-04", "ticker": "AAPL", "close": "110.0"},
]
benchmark = [
    {"date": "2026-11-02", "ticker": "SP500", "close": "200.0"},
    {"date": "2026-11-03", "ticker": "SP500", "close": "202.0"},
    {"date": "2026-11-04", "ticker": "SP500", "close": "210.0"},
]

# 2. Rendement : 100 -> 110 = +10 %, 200 -> 210 = +5 %
r_instrument = calculate_period_return(instrument)
r_benchmark = calculate_period_return(benchmark)
assert abs(r_instrument - 10.0) < 1e-9, r_instrument
assert abs(r_benchmark - 5.0) < 1e-9, r_benchmark

# 3. Base 100 : premier point = 100, dernier = 110 et 105
base_instrument = calculate_base_100(instrument)
base_benchmark = calculate_base_100(benchmark)
assert base_instrument[0]["value"] == 100.0
assert abs(base_instrument[-1]["value"] - 110.0) < 1e-9
assert abs(base_benchmark[-1]["value"] - 105.0) < 1e-9
assert len(base_instrument) == len(instrument)

# 4. Performance relative : +10 % - (+5 %) = +5 points
relative = calculate_relative_performance(r_instrument, r_benchmark)
assert abs(relative - 5.0) < 1e-9, relative

# 5. index_by_date
indexed = index_by_date(instrument)
assert indexed["2026-11-03"]["close"] == "104.0"

# 6. align_series avec des dates différentes (le 03 manque côté SP500,
#    le 05 manque côté AAPL, et les dates arrivent dans le désordre)
aapl = [
    {"date": "2026-11-01", "ticker": "AAPL", "close": "100.0"},
    {"date": "2026-11-03", "ticker": "AAPL", "close": "103.0"},
    {"date": "2026-11-02", "ticker": "AAPL", "close": "102.0"},
    {"date": "2026-11-04", "ticker": "AAPL", "close": "104.0"},
]
sp500 = [
    {"date": "2026-11-04", "ticker": "SP500", "close": "204.0"},
    {"date": "2026-11-01", "ticker": "SP500", "close": "200.0"},
    {"date": "2026-11-02", "ticker": "SP500", "close": "202.0"},
    {"date": "2026-11-05", "ticker": "SP500", "close": "205.0"},
]
aligned_a, aligned_b = align_series(aapl, sp500)
dates_a = [row["date"] for row in aligned_a]
dates_b = [row["date"] for row in aligned_b]
assert dates_a == ["2026-11-01", "2026-11-02", "2026-11-04"], dates_a
assert dates_a == dates_b
assert len(aligned_a) == len(aligned_b) == 3
assert all(row["ticker"] == "AAPL" for row in aligned_a)
assert all(row["ticker"] == "SP500" for row in aligned_b)

# 7. Une série vide doit lever ValueError
try:
    calculate_period_return([])
except ValueError as error:
    print(f"ValueError bien levée pour une série vide : {error}")
else:
    raise AssertionError("calculate_period_return([]) aurait dû lever ValueError")

print(f"Rendement instrument : {r_instrument:+.2f} %")
print(f"Rendement benchmark  : {r_benchmark:+.2f} %")
print(f"Performance relative : {relative:+.2f} points")
print("Tous les tests du module analytics ont réussi.")
