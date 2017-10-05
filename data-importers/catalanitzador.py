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
from dataimport import DataImport
from datetime import datetime

class Catalanitzador(DataImport):

    def extract_data(self):
        url = "https://www.softcatala.org/catalanitzador/response.php"
        print("url->" + url)

        response = urllib.request.urlopen(url)
        data = response.read()
        value = int(data)
        return value

    def transform_data(self, data):
        json_body = [
            {
                "time" : self.store_time(),
                "measurement": "catalanitzador",
                "fields": {
                    "total_downloads" : data
                }
            }
        ]
        return json_body
