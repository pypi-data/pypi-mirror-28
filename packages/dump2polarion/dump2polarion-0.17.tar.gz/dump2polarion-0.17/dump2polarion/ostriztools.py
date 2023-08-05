# -*- coding: utf-8 -*-
"""
Helper functions for handling JSON data from Ostriz.
"""

from __future__ import absolute_import, unicode_literals

import datetime
import io
import json
import os

from collections import OrderedDict

import requests

from dump2polarion import exporter
from dump2polarion.exceptions import Dump2PolarionException


def _get_json(location):
    """Reads JSON data from file or URL."""
    try:
        json_data = requests.get(location)
    except ValueError:
        pass
    else:
        return json.loads(json_data.text, object_pairs_hook=OrderedDict).get('tests')

    location = os.path.expanduser(location)
    if os.path.isfile(location):
        with io.open(location, encoding='utf-8') as json_data:
            try:
                return json.load(json_data, object_pairs_hook=OrderedDict).get('tests')
            except Exception as err:
                raise Dump2PolarionException(
                    "Failed to parse JSON from {}: {}".format(location, err))


def _get_testrun_id(version):
    """Gets testrun id out of the appliance_version file."""
    try:
        build_base = version.strip().split('-')[0].split('_')[0].replace('.', '_')
        zval = int(build_base.split('_')[3])
    except Exception:
        # not in expected format
        raise Dump2PolarionException("Cannot find testrun id")
    if zval < 10:
        pad_build = build_base[-1].zfill(2)
        return build_base[:-1] + pad_build
    return build_base


def _calculate_duration(start_time, finish_time):
    """Calculates how long it took to execute the testcase."""
    if not(start_time and finish_time):
        return 0
    start = datetime.datetime.fromtimestamp(start_time)
    finish = datetime.datetime.fromtimestamp(finish_time)
    duration = finish - start
    return duration.seconds


def _parse_ostriz(ostriz_data):
    """Reads the content of the input JSON and returns testcases results."""
    if not ostriz_data:
        raise Dump2PolarionException("No data to import")
    test_data = []
    data = found_version = None
    for data in ostriz_data.values():
        # make sure we are collecting data for the same appliance version
        if found_version:
            if found_version != data.get('version'):
                continue
        else:
            found_version = data.get('version')
        statuses = data.get('statuses')
        if not statuses:
            continue
        test_data.append(OrderedDict([
            ('verdict', statuses.get('overall')),
            ('title', data.get('test_name')),
            ('time', _calculate_duration(data.get('start_time'), data.get('finish_time')) or 0)
        ]))
    testrun_id = _get_testrun_id(found_version)
    return exporter.ImportedData(results=test_data, testrun=testrun_id)


# pylint: disable=unused-argument
def import_ostriz(location, **kwargs):
    """Reads Ostriz's data and returns imported data."""
    ostriz_data = _get_json(location)
    return _parse_ostriz(ostriz_data)
