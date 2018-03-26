#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Jordi Mas i Hernandez <jmas@softcatala.org>
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


class STT(DataImport):

    def extract_data(self):
        today_date = datetime.now()
        yesterday_date = today_date - timedelta(days=1)
        yesterday = yesterday_date.strftime('%Y-%m-%d')

        url = "https://www.softcatala.org/veu/recognize/stats/?date={0}"
        url = url.format(yesterday)
        print("url->" + url)

        response = urllib.request.urlopen(url)
        json_payload = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
        return int(json_payload['calls'])

    def transform_data(self, data):
        json_body = [
            {
                "time": self.store_time(),
                "measurement": "stt",
                "fields": {
                    "calls": data
                }
            }
        ]
        return json_body
