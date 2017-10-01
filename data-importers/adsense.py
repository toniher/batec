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
from datetime import datetime
from adsense_util import get_account_id
from adsense_util_data_collator import DataCollator
from googleapiclient import discovery
from oauth2client import client, file, tools
import httplib2
import os


class AdSense(DataImport):

    def init(self, name, version, doc, filename, discovery_filename, scope):
        # Name of a file containing the OAuth 2.0 information details
        client_secrets = os.path.join(os.path.dirname(filename),
                                      'client_secrets_adsense.json')

        # Set up a Flow object to be used if we need to authenticate.
        flow = client.flow_from_clientsecrets(client_secrets, scope=scope,
            message=tools.message_if_missing(client_secrets))

        # Prepare credentials, and authorize HTTP object with them.
        # If the credentials don't exist or are invalid run through the native client
        # flow. The Storage object will ensure that if successful the good
        # credentials will get written back to a file.
        storage = file.Storage(name + '.dat')
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            flags = None
            credentials = tools.run_flow(flow, storage, flags)

        http = credentials.authorize(http=httplib2.Http())

        if discovery_filename is None:
            # Construct a service object via the discovery service.
            service = discovery.build(name, version, http=http)
        else:
            # Construct a service object using a local discovery document file.
            with open(discovery_filename) as discovery_file:
                service = discovery.build_from_document(
                    discovery_file.read(),
                    base='https://www.googleapis.com/',
                    http=http)
        return service

    def extract_data(self):

        # Authenticate and construct service.
        service = self.init('adsense', 'v1.4', __doc__, __file__, None,
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
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        json_body = [
            {
                "time": current_time,
                "measurement": "adsense",
                "fields": {
                    "page_views": data['page_views'],
                    "earnings": data['earnings'],
                }
            }
        ]
        return json_body

    def do(self):
        data = self.extract_data()
        json = self.transform_data(data)
        self.load_data(json)
