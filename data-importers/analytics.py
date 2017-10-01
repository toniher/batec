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
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class Analytics(DataImport):

    def get_service(self, api_name, api_version, scope, key_file_location):

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_file_location, scopes=scope)

        service = build(api_name, api_version, credentials=credentials)

        return service

    def get_first_profile_id(self, service):
        accounts = service.management().accounts().list().execute()

        if accounts.get('items'):
            # Get the first Google Analytics account.
            account = accounts.get('items')[0].get('id')

            # Get a list of all the properties for the first account.
            properties = service.management().webproperties().list(
                accountId=account).execute()

        if properties.get('items'):
            # Get the first property id.
            property = properties.get('items')[0].get('id')

        # Get a list of all views (profiles) for the first property.
        profiles = service.management().profiles().list(
            accountId=account,
            webPropertyId=property).execute()

        if profiles.get('items'):
            # return the first view (profile) id.
            return profiles.get('items')[0].get('id')

        return None

    def get_results(self, service, profile_id):
        return service.data().ga().get(
            ids='ga:' + profile_id,
            start_date='yesterday',
            end_date='yesterday',
            metrics='ga:sessions, ga:pageviews').execute()

    def extract_data(self):

        scope = ['https://www.googleapis.com/auth/analytics.readonly']
        key_file_location = 'client_secrets_analytics.json'

        # Authenticate and construct service.
        service = self.get_service('analytics', 'v3', scope, key_file_location)
        profile = self.get_first_profile_id(service)
        results = self.get_results(service, profile)

        data = {}
        data['sessions'] = results.get('rows')[0][0]
        data['page_views'] = results.get('rows')[0][1]
        return data

    def transform_data(self, data):
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        json_body = [
            {
                "time": current_time,
                "measurement": "analytics",
                "fields": {
                    "sessions": data['sessions'],
                    "page_views": data['page_views'],
                }
            }
        ]
        return json_body

    def do(self):
        data = self.extract_data()
        json = self.transform_data(data)
        self.load_data(json)
