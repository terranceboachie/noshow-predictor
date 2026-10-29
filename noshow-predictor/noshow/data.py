"""Synthetic flight data. Swap this for real data later (see README)."""
import numpy as np
import pandas as pd

ROUTES = ["AMS-LHR", "AMS-JFK", "AMS-CDG", "AMS-MAD", "AMS-DXB", "AMS-BCN", "AMS-ATH", "AMS-OSL"]


def generate_flights(n: int = 5000, seed: int = 42) -> pd.DataFrame:
    """Generate n flights with a no-show rate that depends on known factors."""
    rng = np.random.default_rng(seed)
    hour = rng.integers(5, 23, n)
    dow = rng.integers(0, 7, n)
    advance = rng.gamma(4.0, 12.0, n).round(1)
    flex = rng.beta(2, 5, n).round(3)
    connecting = rng.beta(2, 6, n).round(3)

    rate = (
        0.02
        + 0.06 * flex
        + 0.04 * connecting
        + 0.0003 * advance
        + np.where(hour < 7, 0.008, 0.0)
        + np.where(np.isin(dow, [0, 4]), 0.006, 0.0)
        + rng.normal(0, 0.01, n)
    )
    return pd.DataFrame(
        {
            "route": rng.choice(ROUTES, n),
            "hour": hour,
            "day_of_week": dow,
            "month": rng.integers(1, 13, n),
            "booked_passengers": rng.integers(60, 300, n),
            "advance_booking_days": advance,
            "flex_share": flex,
            "connecting_share": connecting,
            "no_show_rate": np.clip(rate, 0.005, 0.25),
        }
    )
