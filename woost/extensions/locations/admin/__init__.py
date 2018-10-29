#-*- coding: utf-8 -*-
u"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from woost.admin.controllers.listingcontroller import ListingController
from . import sections
from .dataexport import LocationsTreeExport

ListingController.exports["x_locations_tree"] = LocationsTreeExport

