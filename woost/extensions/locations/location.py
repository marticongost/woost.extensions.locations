#-*- coding: utf-8 -*-
"""Defines the `Location` class.

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from warnings import warn
from cocktail.iteration import first
from cocktail.translations import translations, get_language
from cocktail.translations.localetranslations \
    import translate_locale_component as base_translate_locale_component
from cocktail import schema
from woost.models import Item
from woost.models.objectio import get_object_ref, resolve_object_ref
from .locationtype import LocationType


class Location(Item):

    members_order = [
        "location_name",
        "location_type",
        "code",
        "parent",
        "locations"
    ]

    location_name = schema.String(
        translated = True,
        descriptive = True,
        required = True,
        indexed = True,
        normalized_index = True,
        full_text_indexed = True,
        listed_by_default = False
    )

    location_type = LocationType(
        required = True,
        indexed = True
    )

    code = schema.String(
        required = True,
        indexed = True,
        text_search = False
    )

    parent = schema.Reference(
        type = "woost.extensions.locations.location.Location",
        bidirectional = True,
        indexed = True,
        cycles_allowed = False
    )

    locations = schema.Collection(
        items = "woost.extensions.locations.location.Location",
        bidirectional = True,
        cascade_delete = True
    )

    def ascend(self, include_self = False):
        """Iterate over the location's ancestors.

        :param include_self: Indicates if the location itself should be included
            in the iteration.
        :type include_self: bool

        :return: An iterable sequence of locations.
        :rtype: `Location`
        """
        ascendant = self if include_self else self.parent
        while ascendant is not None:
            yield ascendant
            ascendant = ascendant.parent

    def descend(self, include_self = False):
        """Iterates over the location's descendants.

        :param include_self: If set to True, the location itself is yielded as
            the first element in the iteration.
        :type include_self: bool

        :return: An iterable sequence containing the location's flattened tree.
        :rtype: `Location`
        """
        if include_self:
            yield self
        for location in self.locations:
            for descendant in location.descend(True):
                yield descendant

    def descends_from(self, ascendant):
        """Indicates if the location descends from a given location.

        :param ascendant: The hypothetical container of the location.
        :type ascendant: `Location`

        :return: True if the location is, or is contained within the given
            location or one of its descendants, False otherwise.
        :rtype: bool
        """
        location = self

        while location is not None:
            if location is ascendant:
                return True
            else:
                location = location.parent

        return False

    def get_ancestor_of_type(self, location_type, include_self = False):
        """Obtains the location's first ancestor of the given type.

        :param location_type: The type of location to obtain; should match one
            of the values accepted by the `location_type` member.
        :type location_type: str

        :param include_self: If set to True, the location itself will be
            returned if it matches the indicated type. Otherwise, the location
            will be skipped and only its ancestors will be considered as
            possible matches.

        :return: The first ancestor of the location that matches the indicated
            type, or None if no such location can be found on the way to the
            tree root.
        :rtype: `Location`
        """
        location = self

        if not include_self:
            location = location.parent

        while location is not None:
            if location.location_type == location_type:
                return location
            location = location.parent

    def get_child_location(self, code, recursive = True):
        """Retrieves the contained location that matches the indicated code.

        :param code: The code of the location to retrieve.
        :type code: str

        :return: The specified location, or None if it wasn't found.
        :rtype: `Location`
        """
        for child in self.locations:
            if child.code == code:
                return child
            if recursive:
                for descendant in child.locations:
                    match = descendant.get_child_location(code)
                    if match:
                        return match

    @classmethod
    def by_code(cls, *code):

        warn(
            "Location.by_code is deprecated, use Location.by_full_path instead",
            DeprecationWarning,
            stacklevel = 2
        )

        if not code or not code[0]:
            raise ValueError(
                "Location.by_code() requires one or more location codes"
            )

        location = first(cls.select([Location.code.equal(code[0])]))

        for x in code[1:]:
            if location is None:
                return None
            location = location.get_child_location(x)

        return location

    @classmethod
    def by_path(cls, *path):

        warn(
            "Location.by_path is deprecated, use Location.by_full_path instead",
            DeprecationWarning,
            stacklevel = 2
        )

        if not path or not path[0]:
            raise ValueError(
                "Location.by_path() requires one or more location codes"
            )

        location = first(cls.select([Location.code.equal(path[0])]))

        for x in path[1:]:
            if location is None:
                return None
            location = location.get_child_location(x, recursive = False)

        return location

    @classmethod
    def by_abs_path(cls, path):

        if not path or not path[0]:
            raise ValueError(
                "Location.by_abs_path() requires one or more location codes"
            )

        location = first(
            cls.select({"code": path[0], "parent": None})
        )

        for x in path[1:]:
            if location is None:
                return None
            location = location.get_child_location(x, recursive = False)

        return location

    @classmethod
    def get_country(cls, iso_code):
        return cls.select({"location_type": "country", "code": iso_code})[0]

    def list_level(self, depth):

        if depth == 1:
            return self.locations
        else:
            descendants = []
            for location in self.locations:
                descendants.extend(location.list_level(depth - 1))
            return descendants


@get_object_ref.implementation_for(Location)
def get_location_ref(location):

    ref = get_object_ref.default(location)

    path = []
    for item in location.ascend(include_self = True):
        if item.code:
            path.append(item.code)
    path.reverse()

    if path:
        ref["@woost.extensions.locations.path"] = path

    return ref

@resolve_object_ref.implementation_for(Location)
def resolve_location_ref(cls, ref):

    obj = resolve_object_ref.default(cls, ref)

    if obj is None:
        path = ref.get("@woost.extensions.locations.path")
        if path:
            obj = cls.by_abs_path(path)

    return obj

# Translation
#------------------------------------------------------------------------------

# Override the translation for locale components to replace country ISO codes
# with human readable descriptions
def translate_locale_component(locale, component, index, language = None):

    if index == 1:
        language = language or get_language()

        location = first(
            Location.select({
                "location_type": "country",
                "code": component
            })
        )
        if location is not None:
            location_name = translations(
                location,
                language = language,
                discard_generic_translation = True
            )

            if not location_name and language != "en":
                location_name = translations(
                    location,
                    "en",
                    discard_generic_translation = True
                )

            return " - " + location_name

    return base_translate_locale_component(
        locale,
        component,
        index,
        language = language
    )

translations.definitions["cocktail.locale_component"] = \
    translate_locale_component

