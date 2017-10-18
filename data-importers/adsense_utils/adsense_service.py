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

from googleapiclient import discovery
from oauth2client import client, file, tools
import httplib2
import os


class AdSenseService():

    def get(name, version, doc, filename, discovery_filename, scope):
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
