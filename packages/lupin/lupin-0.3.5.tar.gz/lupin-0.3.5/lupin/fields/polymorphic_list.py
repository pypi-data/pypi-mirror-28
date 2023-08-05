from . import Field
from ..validators import Type
from ..errors import MissingPolymorphicKey, InvalidPolymorphicType
from ..utils import get_mapping


class PolymorphicList(Field):
    """Field used to handle a list containing objects
    of different types, that need to be loaded, serialized
    in different ways.

    Example:
        PolymorphicList(on="type",
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
        kwargs.setdefault("validators", []).append(Type(list))
        super(PolymorphicList, self).__init__(**kwargs)
        self._on = on
        self._mappings_by_json_value = mappings
        self._mappings_by_type = {mapping.cls: mapping for mapping in mappings.values()}

    def load(self, value):
        """Loads list of python objects from JSON list

        Args:
            value (list): JSON list

        Returns:
            list
        """
        return [self._mappings_by_json_value[item[self._on]].load(item)
                for item
                in value]

    def dump(self, value):
        """Dump list of object

        Args:
            value (list): objects to dump

        Returns:
            list
        """
        return [get_mapping(self._mappings_by_type, item).dump(item)
                for item
                in value]

    def validate(self, value, path):
        """Validate each items of list against nested mapping.

        Args:
            value (list): value to validate
            path (list): JSON path of value
        """
        super(PolymorphicList, self).validate(value, path)
        for item_index, item in enumerate(value):
            item_path = path + [str(item_index)]
            if self._on not in item:
                raise MissingPolymorphicKey(self._on, path)

            obj_type = item[self._on]
            if obj_type not in self._mappings_by_json_value:
                raise InvalidPolymorphicType(invalid_type=obj_type,
                                             supported_types=list(self._mappings_by_json_value.keys()),
                                             path=path+[self._on])

            mapping = self._mappings_by_json_value[obj_type]
            mapping.validate(item, path=item_path)
