#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Xavi Ivars <xavi.ivars@gmail.com>
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
from datetime import datetime, timedelta


class Traductor(DataImport):

    def extract_data(self):
        url = 'https://www.softcatala.org/api/traductor/stats/'
        print("url->" + url)

        response = urllib.request.urlopen(url)
        response_text = response.read().decode(response.info().get_param('charset') or 'utf-8')
        json_payload = json.loads(response_text)

        return json_payload['result']

    def transform_data(self, data):

        sources = {
                "time": self.store_time(),
                "measurement": "traductor_source",
                "fields": { }
        }

        for k,v in data['srcstats']:
            sources['fields'][k] = v

        langs = {
                "time": self.store_time(),
                "measurement": "traductor_lang",
                "fields": { }
        }

        for k,v in data['langstats']:
            langs['fields'][k] = v

        totals = {
            "time": self.store_time(),
            "measurement": "traductor_total",
            "fields": { 'total_translations' : data['total'] }
        }

        return [sources, langs, totals]
