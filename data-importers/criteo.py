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

import yaml
import json
import urllib.request, urllib.parse, urllib.error
from dataimport import DataImport
from datetime import datetime, timedelta


class Criteo(DataImport):

    def load_criteo_yaml(self):
        with open("criteo.yaml", "r") as stream:
            values = yaml.load(stream)
            self.api_token = values['api_token']

    def extract_data(self):
        self.load_criteo_yaml()
        today_date = datetime.now()
        yesterday_date = today_date - timedelta(days=1)
        yesterday = yesterday_date.strftime('%Y-%m-%d')

        baseurl = 'https://publishers.criteo.com//api/2.0/'
        metrics = 'PublisherName;Date;TotalImpression;Revenue'
        url = '{0}stats.json?apitoken={1}&begindate={2}&enddate={3}&metrics='
        url = url.format(baseurl, self.api_token, yesterday, yesterday, metrics)
        print("url->" + url)

        response = urllib.request.urlopen(url)
        response_text = response.read().decode(response.info().get_param('charset') or 'utf-8')
        json_payload = json.loads(response_text)

        revenue = 0
        impressions = 0
        for entry in json_payload:
            revenue += float(entry['revenue']['value'])
            impressions += entry['totalImpression']

        data = {}
        data['revenue'] = revenue
        data['impressions'] = impressions
        return data

    def transform_data(self, data):
        json_body = [
            {
                "time": self.store_time(),
                "measurement": "criteo",
                "fields": {
                    "revenue": float(data['revenue']),
                    "impressions": int(data['impressions'])
                }
            }
        ]
        return json_body
