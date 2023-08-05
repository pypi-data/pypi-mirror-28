# -*- coding: utf-8 -*-
"""Family module for Wikimania wikis."""
#
# (C) Pywikibot team, 2017
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, unicode_literals

__version__ = '$Id: f21f8914bec00f4c4a407a5e32a6b9d01fdebe6f $'

from pywikibot import family


# The Wikimania family
class Family(family.WikimediaFamily):

    """Family class for Wikimania wikis."""

    name = 'wikimania'

    closed_wikis = [
        '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013',
        '2014', '2015', '2016', '2017'
    ]

    def __init__(self):
        """Constructor."""
        super(Family, self).__init__()

        self.langs = {
            '2018': 'wikimania2018.wikimedia.org'
        }

        self.interwiki_forward = 'wikipedia'
