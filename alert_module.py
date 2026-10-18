class InvalidInputError(Exception):
    pass


class AlertEngine:
    def evaluate(self, machine_id, readings, thresholds):
        if not readings:
            raise InvalidInputError("No sensor readings provided.")
        for sensor, value in readings.items():
            if value < 0:
                raise InvalidInputError(f"Negative reading for {sensor}.")

        risk_level = "normal"
        flagged_sensor = None
        for sensor, value in readings.items():
            limit = thresholds.get(sensor, float("inf"))
            if value >= limit:
                risk_level = "critical"
                flagged_sensor = sensor
                break
            elif value >= limit * 0.9:
                risk_level = "warning"
                flagged_sensor = sensor

        work_order_created = risk_level == "critical"
        return {
            "machine_id": machine_id,
            "risk_level": risk_level,
            "flagged_sensor": flagged_sensor,
            "work_order_created": work_order_created,
        }

    def rank_by_risk(self, evaluations):
        risk_order = {"critical": 2, "warning": 1, "normal": 0}
        return sorted(evaluations, key=lambda e: risk_order[e["risk_level"]], reverse=True)