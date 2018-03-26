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

import traceback
import sys
from optparse import OptionParser
from catalanitzador import Catalanitzador
from programs import Programs
from adsense import AdSense
from analytics import Analytics
from tts import TTS
from tm import TM
from dictmutilingual import DictMutilingual
from criteo import Criteo
from traductor import Traductor
from stt import STT


def read_parameters():
    parser = OptionParser()
    parser.add_option(
        '-i',
        '--importers',
        action='store',
        type='string',
        dest='use_importers',
        default='',
        help='To restrict the execution of importers to a comma separated '
        'given list e.g.: (tts, criteo)'
    )

    (options, args) = parser.parse_args()

    use_importers = ''
    if options.use_importers:
        use_importers = options.use_importers.lower().split(',')

    return use_importers


def main():

    print("Imports data into InfluxDB. Use --help for parameters")

    use_importers = read_parameters()

    importers = [Catalanitzador(), Programs(), AdSense(), Analytics(),
                 TTS(), TM(), DictMutilingual(), Criteo(), Traductor(), STT()]

    for importer in importers:
        try:
            if use_importers and type(importer).__name__.lower() not in use_importers:
                continue

            importer.do()

        except Exception as e:
            msg = "Error at importer '{0}': {1}"
            print(msg.format(type(importer).__name__, e))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)


if __name__ == "__main__":
    main()
