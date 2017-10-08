#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import json
import urllib.request, urllib.parse, urllib.error
from dataimport import DataImport

class DictMutilingual(DataImport):

    def extract_data(self):
        url = "https://www.softcatala.org/diccionari-multilingue/api/statistics"
        print("url->" + url)

        response = urllib.request.urlopen(url)
        json_payload = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
        return json_payload

    def transform_data(self, data):
        ca_labels = data['wikidata']['ca_labels'] + data['wikidictionary']['ca_labels']
        ca_descs = data['wikidata']['ca_descs'] + data['wikidictionary']['ca_descs']
        en_labels = data['wikidata']['en_labels'] + data['wikidictionary']['en_labels']
        en_descs = data['wikidata']['en_descs']

        json_body = [
            {
                "time": self.store_time(),
                "measurement": "dict_mutilingual",
                "fields": {
                    "ca_labels": int(ca_labels),
                    "ca_descs": int(ca_descs),
                    "en_labels": int(en_labels),
                    "en_descs": int(en_descs),
                    "images": int(data['wikidata']['images'])
                }
            }
        ]
        return json_body
