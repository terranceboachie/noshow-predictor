from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import Pipeline

from noshow.features import FEATURES, TARGET, build_preprocessor


class NoShowModel:
    """Predicts the share of booked passengers who will not show up."""

    def __init__(self, random_state: int = 42):
        self.pipeline = Pipeline(
            [
                ("prep", build_preprocessor()),
                ("reg", GradientBoostingRegressor(random_state=random_state)),
            ]
        )

    def fit(self, df: pd.DataFrame) -> "NoShowModel":
        self.pipeline.fit(df[FEATURES], df[TARGET])
        return self

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        return np.clip(self.pipeline.predict(df[FEATURES]), 0.0, 1.0)

    def evaluate(self, df: pd.DataFrame) -> dict:
        """MAE of the model vs. a naive baseline that always predicts the mean."""
        baseline = np.full(len(df), df[TARGET].mean())
        return {
            "mae": float(mean_absolute_error(df[TARGET], self.predict(df))),
            "baseline_mae": float(mean_absolute_error(df[TARGET], baseline)),
        }

    def save(self, path: str | Path) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, path)

    @staticmethod
    def load(path: str | Path) -> "NoShowModel":
        return joblib.load(path)
