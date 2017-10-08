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

import urllib.request, urllib.parse, urllib.error
import json
from dataimport import DataImport


class TM(DataImport):

    def extract_data(self):
        url = "https://www.softcatala.org/recursos/tm/api/stats"
        print("url->" + url)

        response = urllib.request.urlopen(url)
        json_payload = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
        data = {}
        data['total_words'] = json_payload['total_words']
        data['projects'] = json_payload['projects']
        return data

    def transform_data(self, data):

        json_body = [
            {
                "time": self.store_time(),
                "measurement": "translation_memory",
                "fields": {
                    "total_words": int(data['total_words']),
                    "projects": int(data['projects']),
                }
            }
        ]
        return json_body
