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

from dataimport import DataImport
from adsense_utils.adsense_util import get_account_id
from adsense_utils.adsense_util_data_collator import DataCollator
from adsense_utils.adsense_service import AdSenseService
from oauth2client import client


class AdSense(DataImport):

    def extract_data(self):
        service = AdSenseService.get('adsense', 'v1.4', __doc__, __file__, None,
          'https://www.googleapis.com/auth/adsense.readonly')

        # Process flags and read their values.
        saved_report_id = 0

        try:
            # Let the user pick account if more than one.
            account_id = get_account_id(service)

            if saved_report_id:
                result = service.accounts().reports().saved().generate(
                    accountId=account_id, savedReportId=saved_report_id).execute()
            else:
                result = service.accounts().reports().generate(
                  accountId=account_id, startDate='today-1d', endDate='today-1d',
                  metric=['PAGE_VIEWS', 'EARNINGS'],
                  dimension=['DATE'],
                  sort=['+DATE']).execute()

            result = DataCollator([result]).collate_data()

            data = {}
            for row in result['rows']:
                for i in range(0, len(row)):
                    header = result['headers'][i]['name'].lower()
                    data[header] = row[i]

            return data

        except client.AccessTokenRefreshError:
            print('The credentials have been revoked or expired,'
                  'please re-run the application to re-authorize')

    def transform_data(self, data):
        json_body = [
            {
                "time": self.store_time(),
                "measurement": "google_adsense",
                "fields": {
                    "page_views": int(data['page_views']),
                    "earnings": float(data['earnings']),
                }
            },
            {
                "time": self.store_time(),
                "measurement": "earnings",
                "fields": {
                    "adsense": float(data['earnings']),
                }
            }
        ]
        return json_body
