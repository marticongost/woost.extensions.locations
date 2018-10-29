#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from cocktail.events import when
from woost.extensions.locations.location import Location
from woost.admin.sections.crud import CRUD
from woost.admin.sections.contentsection import ContentSection


class LocationTreeSection(CRUD):
    model = Location
    tree_children_collection = Location.locations
    exporter = "x_locations_tree"


@when(ContentSection.declared)
def fill(e):
    e.source.append(LocationTreeSection("locations"))

