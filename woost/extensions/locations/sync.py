#-*- coding: utf-8 -*-
"""

.. moduleauthor:: Martí Congost <marti.congost@whads.com>
"""
from time import time
import urllib.request, urllib.parse, urllib.error
import json
from cocktail.iteration import first
from woost.models import Configuration, get_setting
from .location import Location

SECONDS_IN_A_DAY = 60 * 60 * 24

Configuration.x_locations_last_update = None

def should_update():

    last_update = Configuration.instance.x_locations_last_update
    if last_update is None:
        return True

    update_frequency = get_setting("x_locations_update_frequency")
    if update_frequency is None:
        return False

    return time() - last_update >= update_frequency * SECONDS_IN_A_DAY

def sync_locations():
    """Populate the locations database with the data provided by the web
    service.
    """
    service_uri = get_setting("x_locations_service_uri")
    text_data = urllib.request.urlopen(service_uri).read()
    json_data = json.loads(text_data)

    for record in json_data:
        _process_record(record)

    Configuration.instance.x_locations_last_update = time()

def _process_record(record, parent = None, context = None):

    context = context.copy() if context else {}
    code = record["code"]
    location = None

    if "full_code" in context:
        context["full_code"] += "-" + code
    else:
        context["full_code"] = code

    if _should_add_location(record, parent, context):

        # Update an existing location
        if parent:
            location = first(
                child
                for child in parent.locations
                if child.code == code
            )
        else:
            location = first(Location.select([
                Location.parent.equal(None),
                Location.code.equal(code)
            ]))

        # Create a new location
        if location is None:
            location = Location()
            location.parent = parent
            location.code = code
            location.insert()

        location.location_type = record["type"]

        for lang, value in record["name"].items():
            if isinstance(value, bytes):
                value = value.decode("utf-8")
            location.set("location_name", value, lang)

    # Process child records
    children = record.get("locations")
    if children:
        for child_record in children:
            _process_record(child_record, location, context)

def _should_add_location(record, parent, context):

    # Filter by tree subset
    updated_subset = get_setting("x_locations_updated_subset")
    if updated_subset:
        if not context.get("inside_subset") \
        and context["full_code"] not in updated_subset:
            return False
        else:
            context["inside_subset"] = True

    # Filter by location type
    updated_location_types = get_setting("x_locations_updated_location_types")
    if record["type"] not in updated_location_types:
        return False

    return True

