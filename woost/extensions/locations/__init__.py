#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.persistence import transaction
from . import settings, admin
from .location import Location
from .locationtype import LocationType
from .countryreference import CountryReference
from .sync import should_update, sync_locations

def load():
    if should_update():
        transaction(
            sync_locations,
            desist = lambda: not should_update()
        )

