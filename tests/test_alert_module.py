import pytest
from alert_module import AlertEngine, InvalidInputError


@pytest.fixture
def engine():
    return AlertEngine()


def test_reading_within_safe_range_is_normal(engine):
    result = engine.evaluate("M-1", {"vibration": 2.0}, {"vibration": 5.0})
    assert result["risk_level"] == "normal"


def test_reading_exceeds_threshold_is_critical(engine):
    result = engine.evaluate("M-2", {"vibration": 7.0}, {"vibration": 5.0})
    assert result["risk_level"] == "critical"


def test_reading_near_threshold_is_warning(engine):
    result = engine.evaluate("M-3", {"vibration": 4.6}, {"vibration": 5.0})
    assert result["risk_level"] == "warning"


def test_multiple_sensors_flags_breaching_one(engine):
    readings = {"temperature": 90, "vibration": 2}
    thresholds = {"temperature": 80, "vibration": 5}
    result = engine.evaluate("M-4", readings, thresholds)
    assert result["risk_level"] == "critical"
    assert result["flagged_sensor"] == "temperature"


def test_empty_readings_raises_error(engine):
    with pytest.raises(InvalidInputError):
        engine.evaluate("M-5", {}, {"vibration": 5.0})


def test_negative_reading_raises_error(engine):
    with pytest.raises(InvalidInputError):
        engine.evaluate("M-6", {"vibration": -1.0}, {"vibration": 5.0})


def test_risk_score_never_negative(engine):
    result = engine.evaluate("M-7", {"vibration": 0}, {"vibration": 5.0})
    assert result["risk_level"] == "normal"


def test_rank_machines_by_risk_descending(engine):
    evaluations = [
        {"machine_id": "M1", "risk_level": "warning"},
        {"machine_id": "M2", "risk_level": "normal"},
        {"machine_id": "M3", "risk_level": "critical"},
    ]
    ranked = engine.rank_by_risk(evaluations)
    assert [e["machine_id"] for e in ranked] == ["M3", "M1", "M2"]


def test_evaluation_includes_machine_id(engine):
    result = engine.evaluate("M-8", {"vibration": 1.0}, {"vibration": 5.0})
    assert result["machine_id"] == "M-8"


def test_work_order_created_on_critical(engine):
    result = engine.evaluate("M-9", {"vibration": 6.0}, {"vibration": 5.0})
    assert result["work_order_created"] is True