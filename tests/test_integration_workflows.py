import pytest

from alert_module import AlertEngine
from registration_module import MachineNotFoundError, MachineRegistry


@pytest.mark.integration
def test_register_monitor_and_alert_workflow():
    # Arrange
    registry = MachineRegistry()
    engine = AlertEngine()

    # Act
    registry.register("M-201", ["vibration", "temperature"])
    machine = registry.get_machine("M-201")
    result = engine.evaluate(
        "M-201",
        {"vibration": 7.0, "temperature": 70},
        {"vibration": 5.0, "temperature": 80},
    )

    # Assert
    assert machine["sensors"] == ["vibration", "temperature"]
    assert result["risk_level"] == "critical"
    assert result["flagged_sensor"] == "vibration"
    assert result["work_order_created"] is True


@pytest.mark.integration
def test_fleet_ranking_workflow():
    # Arrange
    registry = MachineRegistry()
    engine = AlertEngine()
    machines = [
        ("M-202", 2.0),
        ("M-203", 4.6),
        ("M-204", 6.0),
    ]

    # Act
    evaluations = []
    for machine_id, reading in machines:
        registry.register(machine_id, ["vibration"])
        evaluations.append(
            engine.evaluate(machine_id, {"vibration": reading}, {"vibration": 5.0})
        )
    ranked = engine.rank_by_risk(evaluations)

    # Assert
    assert [item["risk_level"] for item in ranked] == ["critical", "warning", "normal"]


@pytest.mark.integration
def test_failed_registration_never_reaches_monitoring():
    # Arrange
    registry = MachineRegistry()

    # Act
    result = registry.register("M-205", ["humidity"])

    # Assert
    assert result["status"] == "failed"
    with pytest.raises(MachineNotFoundError):
        registry.get_machine("M-205")
