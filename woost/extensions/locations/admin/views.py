#-*- coding: utf-8 -*-
"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from woost.admin.views import Tree, register_view
from woost.extensions.locations.location import Location

locations_tree = Tree(
    "x_locations_tree",
    tree_relations = [Location.locations]
)

register_view(
    locations_tree,
    Location,
    position = "prepend",
    inheritable = False
)

