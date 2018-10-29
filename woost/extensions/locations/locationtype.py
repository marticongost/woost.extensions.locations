#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.translations import translations
from cocktail import schema

translations.load_bundle("woost.extensions.locations.locationtype")


class LocationType(schema.String):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("enumeration", [
            "continent",
            "country",
            "autonomous_community",
            "province",
            "town"
        ])
        kwargs.setdefault("text_search", False)
        kwargs.setdefault("ui_form_control", "cocktail.ui.DropdownSelector")
        schema.String.__init__(self, *args, **kwargs)

