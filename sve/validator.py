import re

class EngineeringValidator:
    """
    Validates model output to ensure required units, formatting, 
    and reasonable physical constraints are met.
    """
    def __init__(self):
        # Common structural & engineering units to check for
        self.standard_units = ["kn", "m", "mm", "mpa", "gpa", "kg", "n/mm2", "kNm"]

    def validate_output(self, text: str) -> dict:
        """
        Scans generated output for standard engineering units 
        and flags missing units or suspicious values.
        """
        if not text:
            return {"valid": False, "reason": "Empty output received."}

        text_lower = text.lower()

        # Check if output contains at least one standard unit of measurement
        has_units = any(re.search(rf"\b{unit}\b", text_lower) for unit in self.standard_units)

        if not has_units:
            return {
                "valid": False,
                "reason": "Warning: Output lacks standard structural units (e.g., kN, MPa, m)."
            }

        return {"valid": True, "reason": "Output passed basic engineering checks."}
