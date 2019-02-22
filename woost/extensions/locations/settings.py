#-*- coding: utf-8 -*-
"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail import schema
from cocktail.translations import translations
from woost.models import add_setting, Configuration
from .locationtype import LocationType

translations.load_bundle("woost.extensions.locations.settings")

add_setting(
    schema.String(
        "x_locations_service_uri",
        required = True,
        default = "http://services.woost.info/locations",
        text_search = False
    ),
    scopes = (Configuration,)
)

add_setting(
    schema.Integer(
        "x_locations_update_frequency",
        min = 1,
        default = 15
    ),
    scopes = (Configuration,)
)

add_setting(
    schema.Collection(
        "x_locations_updated_location_types",
        default = [
            "continent",
            "country",
            "autonomous_community",
            "province",
            "town"
        ],
        items = LocationType(
            required = True
        ),
        text_search = False,
        ui_form_control = "cocktail.ui.CheckList"
    ),
    scopes = (Configuration,)
)

add_setting(
    schema.Collection(
        "x_locations_updated_subset",
        items = schema.String(
            required = True
        ),
        ui_form_control = "cocktail.ui.TextArea"
    ),
    scopes = (Configuration,)
)

