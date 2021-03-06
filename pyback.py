#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Ferhat Geçdoğan All Rights Reserved.
# Distributed under the terms of the MIT License.
#
#

# PyBack : Wayback Machine CLI
#
# github.com/ferhatgec/pyback
#
#

from requests import get
from sys import argv, exit
from re import search

class PyBack:
    def __init__(self):
        self.website = 'https://web.archive.org/save/{website}'
        self.generated = 'https://web.archive.org/web/{time}/{link}/'

        self.website_data = ''

        self.is_captured = False
        self.is_not_found = False
        self.is_generated = False

    def log(self, data, details):
        print(f'ooh! {data}\n'
              '----\n'
              'Details: ',
              details)

        exit(1)

    def generate(self, link):
        if not self.check_internet_connection():
            print('plug your lan cable, seems internet connection not available')
            exit(1)

        print('well! internet connection available')

        self.website = self.website.format(website=link)

        print(self.website)
        self.website_data = get(self.website).text

        if len(self.website_data) > 0:
            print('nice! seems data fetched')
        else:
            print('oops! seems data unfetched, exiting')
            exit(1)

        for line in self.website_data.splitlines():
            if line == '        <h2>Sorry</h2>':
                self.is_captured = True
                continue

            if self.is_captured:
                if 'Cannot resolve host ' in line:
                    self.is_captured = False
                    self.is_not_found = True
                    break

            if '  __wm.wombat' in line:
                lol = search(' {2}__wm.wombat\("(.*?)","(.*?)","', self.website_data)

                self.generated = self.generated.format(time=lol[2], link=link)

                if not lol is None:
                    self.is_generated = True

                break

            continue

        if self.is_generated:
            print('yes! -> ', self.generated + '%2f')
        elif self.is_captured:
            self.log('this url already captured 10 times.',
                     'This URL has been already captured 10 times today. '
                     'Please email us at "info@archive.org" if you would like to discuss this more.')
        elif self.is_not_found:
            self.log('this url not found.',
                     f'Cannot resolve host {link}.')
        else:
            print('oops!')

    # From github.com/ferhatgec/pycliwidget
    @staticmethod
    def check_internet_connection() -> bool:
        try:
            import httplib
        except:
            import http.client as httplib

        connection = httplib.HTTPConnection("www.google.com", timeout=1)

        try:
            connection.request("HEAD", "/")
            connection.close()

            return True
        except:
            connection.close()

            return False


if len(argv) < 2:
    print('PyBack - Wayback Machine CLI\n'
          '---\n'
          'pyback {link}')

    exit(1)

init = PyBack()
init.generate(argv[1])
