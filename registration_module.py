VALID_SENSOR_TYPES = {"vibration", "temperature", "pressure"}


class MachineAlreadyExistsError(Exception):
    pass


class NoSensorsLinkedError(Exception):
    pass


class MachineNotFoundError(Exception):
    pass


class MachineRegistry:
    def __init__(self):
        self._machines = {}

    def register(self, machine_id, sensors):
        if not machine_id:
            return {"status": "failed", "message": "Invalid machine_id."}
        if machine_id in self._machines:
            raise MachineAlreadyExistsError(f"{machine_id} already registered.")
        if not sensors:
            raise NoSensorsLinkedError("At least one sensor must be linked.")
        for s in sensors:
            if s not in VALID_SENSOR_TYPES:
                return {"status": "failed", "message": f"Invalid sensor type '{s}'."}
        self._machines[machine_id] = {"sensors": sensors, "status": "active"}
        return {"status": "success", "machine_id": machine_id}

    def get_machine(self, machine_id):
        if machine_id not in self._machines:
            raise MachineNotFoundError(f"{machine_id} not found.")
        return self._machines[machine_id]