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

from sregistry.logger import bot
import sys
import pwd
import os

def main(args, parser, subparser):
    '''sharing an image means sending a remote share from an image you
       control to a contact, usually an email.
    '''

    from sregistry.main import Client as cli
    images = args.image

    if not isinstance(images,list):
        images = [images]

    for image in images:
        print(image)
        cli.share(image, share_to=args.share_to)
