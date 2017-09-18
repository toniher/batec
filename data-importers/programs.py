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
from datetime import datetime, timedelta

class Programs(DataImport):

    def extract_data(self):
        today_date = datetime.utcnow()
        yesterday_date = today_date - timedelta(days=1)
        today = today_date.strftime('%Y-%m-%d')
        yesterday = yesterday_date.strftime('%Y-%m-%d')

        url = "https://www.softcatala.org/top_so.php?type=top&from={0}&to={1}&count=99999"
        url = url.format(yesterday, today)
        print("url->" + url)

        response = urllib.request.urlopen(url)
        json_payload = json.loads(response.read().decode(response.info().get_param('charset') or 'utf-8'))
        counts = {}

        for platform in json_payload:
            total = 0

            for program in json_payload[platform]:
                cnt = int(program['total'])
                total = total + cnt

            counts[platform] = total

        return counts

    def transform_data(self, data):
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        json_dict = {}
        json_dict['time'] = current_time
        json_dict['measurement'] = 'programs'
        json_dict['fields'] = data
        json_list = []
        json_list.append(json_dict)
        return json_list

    def do(self):
        data = self.extract_data()
        json = self.transform_data(data)
        self.load_data(json)
