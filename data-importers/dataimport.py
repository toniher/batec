# -*- coding: utf-8 -*-
#
#  Copyrignt (C) 2017 Jordi Mas <jmas@softcatala.org>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor,
#  Boston, MA 02110-1301, USA.

from abc import ABCMeta, abstractmethod
from influxdb import InfluxDBClient

class DataImport(metaclass=ABCMeta):

    @abstractmethod
    def extract_data(self):
        pass

    def load_data(self, json):
        user = 'root'
        password = 'root'
        dbname = 'demo'
        host='localhost'
        port=8086
        client = InfluxDBClient(host, port, user, password, dbname)
        print("wrote: " + str(json))
        client.write_points(json)
 
    @abstractmethod
    def do(self):
        pass


