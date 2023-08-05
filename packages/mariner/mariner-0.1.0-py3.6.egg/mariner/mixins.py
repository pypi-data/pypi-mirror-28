import json
from typing import Any, Dict


class ToDictMixin:
    """Provide to_dict method for objects."""

    def to_dict(self):
        """Return dictionary representation of object."""
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict: Dict[Any, Any]) -> Dict[Any, Any]:
        """Traverse dictionary recursively.

        Params:
            instance_dictionary: A dictionary to traverse.

        Returns: Dictionary representation of object.
        """
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key: Any, value: Any) -> Any:
        """Return value for given key.

         Params:
            key: Dictionary key.
            value: Value for the key.

        Returns:
            Value for the given key.
        """
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value


class JsonMixin:
    """Serialize and deserialize from JSON."""
    @classmethod
    def from_json(cls: Any, data: Dict[str, str]) -> Any:
        """Deserialize object from JSON.

        Params:
            cls: Object class.
            data: Dictionary represantatio of class.
        """
        kwargs = json.loads(data)
        return cls(**kwargs)

    def to_json(self) -> Dict[str, str]:
        """Serialize object into JSON.

        Returns:
            JSON representation of object.
        """
        return json.dumps(self.to_dict())
