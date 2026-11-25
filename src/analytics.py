"""Module d'analyse financière de MarketPulse (TD07).

Fonctions réutilisables pour comparer un instrument (ex. AAPL) à son
benchmark (ex. SP500). Chaque observation est un dictionnaire au format
canonique MarketPulse : date, ticker, open, high, low, close, volume.

Le module ne lit aucun fichier et n'affiche rien : il ne fait que calculer.
"""


def index_by_date(prices):
    """Crée un dictionnaire {date: observation} à partir d'une liste d'observations."""
    return {row["date"]: row for row in prices}


def align_series(instrument_prices, benchmark_prices):
    """Conserve uniquement les dates communes aux deux séries, triées.

    Renvoie deux listes de même longueur, avec les mêmes dates dans le même ordre.
    """
    a = index_by_date(instrument_prices)
    b = index_by_date(benchmark_prices)
    common_dates = sorted(set(a) & set(b))
    aligned_a = [a[date] for date in common_dates]
    aligned_b = [b[date] for date in common_dates]
    return aligned_a, aligned_b


def calculate_period_return(prices):
    """Rendement de la période en % : (prix final / prix initial - 1) x 100."""
    if not prices:
        raise ValueError("Cannot compute return on an empty series.")
    first_close = float(prices[0]["close"])
    last_close = float(prices[-1]["close"])
    if first_close == 0.0:
        raise ZeroDivisionError("Initial price cannot be zero.")
    return ((last_close / first_close) - 1.0) * 100.0


def calculate_base_100(prices):
    """Transforme une série en indice base 100 : (prix t / prix initial) x 100.

    Renvoie une liste de dictionnaires {"date": ..., "value": ...}.
    """
    if not prices:
        raise ValueError("Cannot compute base 100 on an empty series.")
    first_close = float(prices[0]["close"])
    if first_close == 0.0:
        raise ZeroDivisionError("Initial price cannot be zero.")
    return [
        {"date": row["date"], "value": (float(row["close"]) / first_close) * 100.0}
        for row in prices
    ]


def calculate_relative_performance(instrument_return, benchmark_return):
    """Performance relative en points de pourcentage : rendement instrument - rendement indice."""
    return instrument_return - benchmark_return
