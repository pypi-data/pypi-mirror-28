# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2014-2017 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""DoJSON rules for MARC fields in 2xx."""

from __future__ import absolute_import, division, print_function

import langdetect

from dojson import utils

from inspire_utils.helpers import force_list

from ..model import hep, hep2marc
from ...utils import force_single_element, normalize_date_aggressively


@hep.over('titles', '^(210|242|245|246|247)..')
def titles(self, key, value):
    """Populate the ``titles`` key.

    Also populates the ``title_translations`` key through side effects.
    """
    def is_main_title(key):
        return key.startswith('245')

    def is_translated_title(key):
        return key.startswith('242')

    titles = self.setdefault('titles', [])
    values = force_list(value)
    for val in values:
        title_obj = {
            'title': val.get('a'),
            'subtitle': force_single_element(val.get('b')),  # FIXME: #1484
            'source': val.get('9'),
        }
        if is_main_title(key):
            titles.insert(0, title_obj)
        elif is_translated_title(key):
            title = val.get('a')
            if title:
                lang = langdetect.detect(title)
                if lang:
                    title_obj['language'] = lang
                    self.setdefault('title_translations', []).append(title_obj)
        else:
            titles.append(title_obj)

    return titles


@hep2marc.over('246', '^titles$')
def titles2marc(self, key, value):
    """Populate the ``246`` MARC field.

    Also populates the ``245`` MARC field through side effects.
    """
    def get_transformed_title(val):
        return {
            'a': val.get('title'),
            'b': val.get('subtitle'),
            '9': val.get('source'),
        }

    values = force_list(value)
    if values:
        # Anything but the first element is the main title
        self['245'] = [get_transformed_title(values[0])]
    return [get_transformed_title(el) for el in values[1:]]


@hep2marc.over('242', '^title_translations$')
def title_translations2marc(self, key, value):
    """Populate the ``242`` MARC field."""
    def get_transformed_title(val):
        return {
            'a': val.get('title'),
            'b': val.get('subtitle'),
            '9': val.get('source'),
        }

    values = force_list(value)
    return [get_transformed_title(el) for el in values]


@hep.over('editions', '^250..')
@utils.flatten
@utils.for_each_value
def editions(self, key, value):
    """Populate the ``editions`` key."""
    return force_list(value.get('a'))


@hep2marc.over('250', '^editions$')
@utils.for_each_value
def editions2marc(self, key, value):
    """Populate the ``250`` MARC field."""
    return {'a': value}


@hep.over('imprints', '^260..')
@utils.for_each_value
def imprints(self, key, value):
    """Populate the ``imprints`` key."""
    return {
        'place': value.get('a'),
        'publisher': value.get('b'),
        'date': normalize_date_aggressively(value.get('c')),
    }


@hep2marc.over('260', '^imprints$')
@utils.for_each_value
def imprints2marc(self, key, value):
    """Populate the ``260`` MARC field."""
    return {
        'a': value.get('place'),
        'b': value.get('publisher'),
        'c': value.get('date'),
    }


@hep.over('preprint_date', '^269..')
def preprint_date(self, key, value):
    """Populate the ``preprint_date`` key."""
    return normalize_date_aggressively(value.get('c'))


@hep2marc.over('269', '^preprint_date$')
@utils.for_each_value
def preprint_date2marc(self, key, value):
    """Populate the ``269`` MARC field."""
    return {'c': value}
