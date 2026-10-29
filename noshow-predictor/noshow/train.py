import argparse
import json
from pathlib import Path

from sklearn.model_selection import train_test_split

from noshow.data import generate_flights
from noshow.model import NoShowModel


def main(n: int = 5000, out: str = "artifacts") -> dict:
    df = generate_flights(n)
    train, test = train_test_split(df, test_size=0.2, random_state=42)
    model = NoShowModel().fit(train)
    metrics = model.evaluate(test)
    model.save(Path(out) / "model.joblib")
    (Path(out) / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print(metrics)
    return metrics


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=5000)
    p.add_argument("--out", default="artifacts")
    a = p.parse_args()
    main(a.n, a.out)
