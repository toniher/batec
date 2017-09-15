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
import yaml

class DataImport(metaclass=ABCMeta):

    def __init__(self):
        self.load_yaml()

    @abstractmethod
    def extract_data(self):
        pass

    def load_yaml(self):
        stream = open("influx-db.yaml", "r")
        values = yaml.load(stream)
        self.user = values['user']
        self.password = values['password']
        self.dbname = values['dbname']
        self.host = values['host']
        self.port = values['port']
       
    def load_data(self, json):
        client = InfluxDBClient(self.host, self.port, self.user, self.password, self.dbname)
        print("wrote: " + str(json))
        result = client.write_points(json)
        print("result: " + str(result))

    @abstractmethod
    def do(self):
        pass


