from noshow.data import generate_flights
from noshow.model import NoShowModel


def test_data_shape_and_range():
    df = generate_flights(200)
    assert len(df) == 200
    assert df["no_show_rate"].between(0, 1).all()


def test_model_beats_baseline():
    df = generate_flights(1500)
    m = NoShowModel().fit(df.iloc[:1200])
    metrics = m.evaluate(df.iloc[1200:])
    assert metrics["mae"] < metrics["baseline_mae"]


def test_save_and_load(tmp_path):
    df = generate_flights(300)
    m = NoShowModel().fit(df)
    m.save(tmp_path / "m.joblib")
    loaded = NoShowModel.load(tmp_path / "m.joblib")
    assert (m.predict(df) == loaded.predict(df)).all()
