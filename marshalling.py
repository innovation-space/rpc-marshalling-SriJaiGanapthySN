import json
from typing import Dict, Any, List


def validate_types(data: Dict[str, Any], schema: Dict[str, type]) -> None:
    for field_name, expected_type in schema.items():
        if field_name not in data:
            raise KeyError(f"Missing required field: '{field_name}'")

        value = data[field_name]

        if not isinstance(value, expected_type):
            raise TypeError(
                f"Type error for field '{field_name}': "
                f"expected {expected_type.__name__}, got {type(value).__name__} "
                f"(value: {repr(value)})"
            )

        if field_name == "grades" and expected_type == list:
            for i, grade in enumerate(value):
                if not isinstance(grade, int):
                    raise TypeError(
                        f"Type error for field 'grades[{i}]': "
                        f"expected int, got {type(grade).__name__} "
                        f"(value: {repr(grade)})"
                    )


def marshal(obj: Any) -> Dict[str, Any]:
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    elif isinstance(obj, dict):
        return obj
    else:
        raise TypeError(f"Cannot marshal object of type {type(obj).__name__}")


def unmarshal(data: Dict[str, Any], target_class: type) -> Any:
    if hasattr(target_class, 'from_dict'):
        return target_class.from_dict(data)
    else:
        raise TypeError(f"Cannot unmarshal to class {target_class.__name__}")


def serialize_to_json(data: Dict[str, Any]) -> str:
    return json.dumps(data)


def deserialize_from_json(json_str: str) -> Dict[str, Any]:
    return json.loads(json_str)


STUDENT_PROFILE_SCHEMA = {
    "name": str,
    "id": int,
    "grades": list
}


def validate_student_profile(data: Dict[str, Any]) -> None:
    print(f"[Marshalling] Validating StudentProfile data: {data}")
    validate_types(data, STUDENT_PROFILE_SCHEMA)
    print("[Marshalling] Validation successful - all types are correct")
