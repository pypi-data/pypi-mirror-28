from . import Field
from ..validators import Type
from ..errors import MissingPolymorphicKey, InvalidPolymorphicType
from ..utils import get_mapping


class PolymorphicObject(Field):
    """Field used to handle a key that can contain multiple object types

    Example:
        PolymorphicObject(on="type",
                          mappings={
                              "diamond": diamond_mapping,
                              "painting": painting_mapping
                          })
    """
    def __init__(self, on, mappings, **kwargs):
        """
        Args:
            on (str): JSON key used to get the object type
            mappings (dict): mapping used for each values used for the `on` key
        """
        kwargs.setdefault("validators", []).append(Type(dict))
        super(PolymorphicObject, self).__init__(**kwargs)
        self._on = on
        self._mappings_by_json_value = mappings
        self._mappings_by_type = {mapping.cls: mapping for mapping in mappings.values()}

    def load(self, value):
        """Loads python objects from JSON object

        Args:
            value (dict): JSON data

        Returns:
            object
        """
        if value is None:
            return None
        return self._mappings_by_json_value[value[self._on]].load(value)

    def dump(self, value):
        """Dump object

        Args:
            value (object): objects to dump

        Returns:
            dict
        """
        mapping = get_mapping(self._mappings_by_type, value)
        return mapping.dump(value)

    def validate(self, value, path):
        """Validate each items of list against nested mapping.

        Args:
            value (list): value to validate
            path (list): JSON path of value
        """
        super(PolymorphicObject, self).validate(value, path)
        if self._on not in value:
            raise MissingPolymorphicKey(self._on, path)

        obj_type = value[self._on]
        if obj_type not in self._mappings_by_json_value:
            raise InvalidPolymorphicType(invalid_type=obj_type,
                                         supported_types=list(self._mappings_by_json_value.keys()),
                                         path=path+[self._on])

        mapping = self._mappings_by_json_value[value[self._on]]
        mapping.validate(value, path=path)
