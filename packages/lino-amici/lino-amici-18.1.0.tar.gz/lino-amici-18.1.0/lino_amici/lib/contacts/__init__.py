# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""
Lino Amici extension of :mod:`lino_xl.lib.contacts`.

.. autosummary::
   :toctree:

    models

"""

from lino_xl.lib.contacts import Plugin


class Plugin(Plugin):
    
    extends_models = ['Person', 'Company']

    use_vcard_export = True
    
