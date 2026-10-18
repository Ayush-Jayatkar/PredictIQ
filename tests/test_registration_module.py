import pytest
from registration_module import (
    MachineRegistry,
    MachineAlreadyExistsError,
    NoSensorsLinkedError,
    MachineNotFoundError,
)


@pytest.fixture
def registry():
    return MachineRegistry()


def test_register_new_machine_successfully(registry):
    result = registry.register("M-101", ["vibration", "temperature"])
    assert result["status"] == "success"
    assert result["machine_id"] == "M-101"


def test_register_duplicate_machine_raises_error(registry):
    registry.register("M-102", ["vibration"])
    with pytest.raises(MachineAlreadyExistsError):
        registry.register("M-102", ["temperature"])


def test_register_rejects_empty_machine_id(registry):
    result = registry.register("", ["vibration"])
    assert result["status"] == "failed"
    assert "machine_id" in result["message"]


def test_register_rejects_no_sensors(registry):
    with pytest.raises(NoSensorsLinkedError):
        registry.register("M-103", [])


def test_register_rejects_invalid_sensor_type(registry):
    result = registry.register("M-104", ["humidity"])
    assert result["status"] == "failed"
    assert "sensor type" in result["message"]


def test_get_registered_machine_returns_record(registry):
    registry.register("M-105", ["pressure"])
    machine = registry.get_machine("M-105")
    assert machine["sensors"] == ["pressure"]
    assert machine["status"] == "active"


def test_get_unregistered_machine_raises_error(registry):
    with pytest.raises(MachineNotFoundError):
        registry.get_machine("M-999")


def test_machine_linked_to_multiple_sensors(registry):
    registry.register("M-106", ["vibration", "temperature", "pressure"])
    machine = registry.get_machine("M-106")
    assert len(machine["sensors"]) == 3