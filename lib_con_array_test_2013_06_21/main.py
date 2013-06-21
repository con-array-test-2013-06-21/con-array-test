# -*- mode: python; coding: utf-8 -*-
#
# Copyright 2013 Andrej A Antonov <polymorphm@gmail.com>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

assert str is not bytes

import argparse
from . import con_array_test

def main():
    parser = argparse.ArgumentParser(
            description='``con-array-test`` is utility for checking -- how is working a HTTP-server '
                    'in situation with big array of connections.')
    
    parser.add_argument(
            'hostname', metavar='HOSTNAME',
            help='hostname or IP (IPv6 or IPv4) address to testing HTTP-server',
            )
    
    parser.add_argument(
            'con_count', metavar='CON-COUNT', type=int,
            help='count of connections. size of connections array',
            )
    
    parser.add_argument(
            'delay', metavar='DELAY', type=float,
            help='delay between connection operations',
            )
    
    args = parser.parse_args()
    
    con_array_test.con_array_test(args.hostname, args.con_count, args.delay)
