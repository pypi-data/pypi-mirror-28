'''

Copyright (C) 2017 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2017 Vanessa Sochat.

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
from dateutil import parser
import hashlib
import os
import re


def print_date(date, format='%b %d, %Y %I:%M%p'):
    datetime_object = parser.parse(date)
    return datetime_object.strftime(format)


def get_image_hash(image_path):
    '''return an md5 hash of the file based on a criteria level. This
    is intended to give the file a reasonable version.
    :param image_path: full path to the singularity image
    '''
    hasher = hashlib.md5()
    with open(image_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def parse_image_name(image_name, tag=None, version=None, 
                                 defaults=True, ext="simg",
                                 default_collection="library",
                                 default_tag="latest"):

    '''return a collection and repo name and tag
    for an image file.
    
    Parameters
    =========
    image_name: a user provided string indicating a collection,
                image, and optionally a tag.
    tag: optionally specify tag as its own argument
         over-rides parsed image tag
    defaults: use defaults "latest" for tag and "library"
              for collection. 
    '''
    result = dict()
    image_name = re.sub('[.](img|simg)','',image_name).lower()
    image_name = re.split('/', image_name, 1)

    # User only provided an image
    if len(image_name) == 1:
        collection = ''
        if defaults is True:
            collection = default_collection
        image_name = image_name[0]

    # Collection and image provided
    elif len(image_name) >= 2:
        collection = image_name[0]
        image_name = image_name[1]
    
    # Is there a version?
    image_name = image_name.split('@')
    if len(image_name) > 1: 
        version = image_name[1]
    image_name = image_name[0]

    # Is there a tag?
    image_name = image_name.split(':')

    # No tag in provided string
    if len(image_name) > 1: 
        tag = image_name[1]
    image_name = image_name[0]
    
    # If still no tag, use default or blank
    if tag is None and defaults is True:
        tag = default_tag

    # Piece together the filename
    uri = "%s/%s" % (collection, image_name)    
    url = uri
    if tag is not None:
        uri = "%s:%s" % (uri, tag)
    if version is not None:
        uri = "%s@%s" % (uri, version)

    storage = "%s.%s" %(uri, ext)
    result = {"collection": collection,
              "image": image_name,
              "url": url,
              "tag": tag,
              "version": version,
              "storage": storage,
              "uri": uri}

    return result

def format_container_name(name, special_characters=None):
    '''format_container_name will take a name supplied by the user,
    remove all special characters (except for those defined by "special-characters"
    and return the new image name.
    '''
    if special_characters is None:
        special_characters = []
    return ''.join(e.lower()
                   for e in name if e.isalnum() or e in special_characters)


def remove_uri(container):
    '''remove_uri will remove the uri, and if a particular uri
docker:// or shub:// from the uri
    '''
    accepted_uris = ['docker', 
                     'shub', 
                     'registry', 
                     'nvidia', 
                     'google-storage',
                     'google-drive']

    return container.replace('docker://', '').replace('shub://', '')
