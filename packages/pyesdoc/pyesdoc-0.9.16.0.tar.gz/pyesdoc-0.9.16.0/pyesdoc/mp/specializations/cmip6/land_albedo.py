"""A realm process sepecialization.

For further information goto http://wordpress.es-doc.org/cmip6-model-specializations.

"""
# --------------------------------------------------------------------
# INTERNAL (do not change)
# --------------------------------------------------------------------
from collections import OrderedDict

DETAILS = OrderedDict()
ENUMERATIONS = OrderedDict()

# --------------------------------------------------------------------
# CONTACT: Set to realm specialization co-ordinator.
# --------------------------------------------------------------------
CONTACT = 'David Hassell'

# --------------------------------------------------------------------
# AUTHORS: Set to realm specialization authors (comma delimited).
# --------------------------------------------------------------------
AUTHORS = 'David Hassell'

# --------------------------------------------------------------------
# QUALITY CONTROL STATUS: Set to 'draft' or 'complete'
# --------------------------------------------------------------------
QC_STATUS = 'draft'

# --------------------------------------------------------------------
# DESCRIPTION: Short description of the specialization.
# --------------------------------------------------------------------
DESCRIPTION = 'Land surface albedo'

# --------------------------------------------------------------------
# ALBEDO: top level
# --------------------------------------------------------------------
DETAILS['toplevel'] = {
    'description': 'General properties in land surface albedo',
    'properties': [
        ('overview', 'str', '1.1',
             'Overview of albedo in land surface'),
        ('tiling', 'str', '0.1',
             'Describe the albedo tiling, if any.'),
    ],
}

# --------------------------------------------------------------------
# ALBEDO: ENUMERATIONS
# --------------------------------------------------------------------

ENUMERATIONS['phenology_types'] = {
    'description': 'Description of the treatment of vegetation phenolo]gy',
    'is_open': True,
    'members': [
        ('prognostic', None),
        ('diagnostic (vegetation map)', None),
        ]
}

ENUMERATIONS['leaf_area_index_types'] = {
    'description': 'Describe the treatment of the leaf area index',
    'is_open': True,
    'members': [
        ('prescribed', None),
        ('prognostic', None),
        ('diagnostic', None),
        ]
    }

ENUMERATIONS['biomass_types'] = {
    'description': 'Describe the treatment of vegetation biomass',
    'is_open': True,
    'members': [
        ('prognostic', None),
        ('diagnostic', None),
        ]
    }

ENUMERATIONS['biogeography_types'] = {
    'description': 'Describe the treatment of vegatation biogeography',
    'is_open': True,
    'members': [
        ('prognostic', None),
        ('diagnostic', None),
        ]
    }

ENUMERATIONS['stomatal_resistance_types'] = {
    'description': 'Specify the dependancies on vegetation stomatal resistance',
    'is_open': True,
    'members': [
        ('light', None),
        ('temperature', None),
        ('water availability', None),
        ('CO2', None),
        ('O3', None),
    ]
}
