#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from woost.admin.models.dataexport import TreeExport
from woost.extensions.locations.location import Location


class LocationsTreeExport(TreeExport):

    children_collection = Location.locations

    def get_tree_roots(self):
        return Location.select(
            Location.parent.equal(None),
            order = "location_name"
        )

