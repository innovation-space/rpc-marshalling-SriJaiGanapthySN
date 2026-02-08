"""
Marshalling Layer for RPC Framework

This module provides marshalling (serialization) and unmarshalling (deserialization)
functionality for converting objects to/from dictionary format for network transmission.

It also includes type validation to ensure data integrity during unmarshalling.
"""

import json
from typing import Dict, Any, List


def validate_types(data: Dict[str, Any], schema: Dict[str, type]) -> None:
    """
    Validate that incoming data matches the expected types.
    
    This function checks the incoming data on the server side and raises
    a TypeError if any field has an incorrect type (e.g., string where int is expected).
    
    Args:
        data: The dictionary data to validate
        schema: A dictionary mapping field names to their expected types
        
    Raises:
        TypeError: If a field has an incorrect type
        KeyError: If a required field is missing
        
    Example:
        >>> schema = {"name": str, "id": int, "grades": list}
        >>> validate_types({"name": "John", "id": 123, "grades": [90, 85]}, schema)  # OK
        >>> validate_types({"name": "John", "id": "123", "grades": [90]}, schema)  # Raises TypeError
    """
    for field_name, expected_type in schema.items():
        # Check if field exists
        if field_name not in data:
            raise KeyError(f"Missing required field: '{field_name}'")
        
        value = data[field_name]
        
        # Check type
        if not isinstance(value, expected_type):
            raise TypeError(
                f"Type error for field '{field_name}': "
                f"expected {expected_type.__name__}, got {type(value).__name__} "
                f"(value: {repr(value)})"
            )
        
        # Additional validation for list of integers (grades)
        if field_name == "grades" and expected_type == list:
            for i, grade in enumerate(value):
                if not isinstance(grade, int):
                    raise TypeError(
                        f"Type error for field 'grades[{i}]': "
                        f"expected int, got {type(grade).__name__} "
                        f"(value: {repr(grade)})"
                    )


def marshal(obj: Any) -> Dict[str, Any]:
    """
    Marshal (serialize) an object to a dictionary format.
    
    This function converts a Python object to a dictionary that can be
    serialized to JSON for network transmission.
    
    Args:
        obj: The object to marshal (must have a to_dict() method)
        
    Returns:
        Dictionary representation of the object
    """
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    elif isinstance(obj, dict):
        return obj
    else:
        raise TypeError(f"Cannot marshal object of type {type(obj).__name__}")


def unmarshal(data: Dict[str, Any], target_class: type) -> Any:
    """
    Unmarshal (deserialize) a dictionary to an object.
    
    This function converts a dictionary (received from network) back to
    a Python object of the specified class.
    
    Args:
        data: The dictionary data to unmarshal
        target_class: The class to create an instance of (must have from_dict() method)
        
    Returns:
        An instance of target_class
    """
    if hasattr(target_class, 'from_dict'):
        return target_class.from_dict(data)
    else:
        raise TypeError(f"Cannot unmarshal to class {target_class.__name__}")


def serialize_to_json(data: Dict[str, Any]) -> str:
    """
    Serialize a dictionary to JSON string.
    
    Args:
        data: Dictionary to serialize
        
    Returns:
        JSON string representation
    """
    return json.dumps(data)


def deserialize_from_json(json_str: str) -> Dict[str, Any]:
    """
    Deserialize a JSON string to dictionary.
    
    Args:
        json_str: JSON string to deserialize
        
    Returns:
        Dictionary parsed from JSON
    """
    return json.loads(json_str)


# Schema definitions for different object types
STUDENT_PROFILE_SCHEMA = {
    "name": str,
    "id": int,
    "grades": list
}


def validate_student_profile(data: Dict[str, Any]) -> None:
    """
    Validate incoming StudentProfile data.
    
    This is a convenience function that validates data against the
    StudentProfile schema.
    
    Args:
        data: Dictionary data representing a StudentProfile
        
    Raises:
        TypeError: If any field has an incorrect type
        KeyError: If a required field is missing
    """
    print(f"[Marshalling] Validating StudentProfile data: {data}")
    validate_types(data, STUDENT_PROFILE_SCHEMA)
    print("[Marshalling] Validation successful - all types are correct")
