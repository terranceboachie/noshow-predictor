from fastapi.testclient import TestClient

from noshow import api
from noshow.data import generate_flights
from noshow.model import NoShowModel

FLIGHT = {"route": "AMS-LHR", "hour": 8, "day_of_week": 4, "month": 6,
          "booked_passengers": 180, "advance_booking_days": 40,
          "flex_share": 0.3, "connecting_share": 0.2}


def make_client(tmp_path, monkeypatch):
    NoShowModel().fit(generate_flights(500)).save(tmp_path / "m.joblib")
    monkeypatch.setenv("MODEL_PATH", str(tmp_path / "m.joblib"))
    api.get_model.cache_clear()
    return TestClient(api.app)


def test_health(tmp_path, monkeypatch):
    assert make_client(tmp_path, monkeypatch).get("/health").json() == {"status": "ok"}


def test_predict(tmp_path, monkeypatch):
    r = make_client(tmp_path, monkeypatch).post("/predict", json=FLIGHT)
    assert r.status_code == 200
    assert 0 <= r.json()["no_show_rate"] <= 1


def test_predict_validation(tmp_path, monkeypatch):
    bad = {**FLIGHT, "hour": 99}
    assert make_client(tmp_path, monkeypatch).post("/predict", json=bad).status_code == 422
