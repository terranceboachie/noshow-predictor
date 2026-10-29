from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

CATEGORICAL = ["route"]
NUMERIC = ["hour", "day_of_week", "month", "booked_passengers",
           "advance_booking_days", "flex_share", "connecting_share"]
FEATURES = CATEGORICAL + NUMERIC
TARGET = "no_show_rate"


def build_preprocessor() -> ColumnTransformer:
    """One-hot encode routes (unknown routes ignored), pass numerics through."""
    return ColumnTransformer(
        [("route", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL)],
        remainder="passthrough",
    )
