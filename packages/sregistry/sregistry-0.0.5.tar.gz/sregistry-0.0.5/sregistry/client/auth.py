'''

Copyright (C) 2017 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2016-2017 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

from sregistry.utils import read_json
from sregistry.logger import bot
from sregistry.auth import read_client_secrets
import sys
import pwd
import os


def main(args,parser,subparser):

    # Load the user auth secrets
    try:
        secrets = read_client_secrets(args.secrets)
        token = secrets['token']
        user = secrets['username']
    except:
        subparser.print_help()
