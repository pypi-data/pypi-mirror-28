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

def get_image_name(manifest, extension='simg', use_commit=False, use_hash=False):
    '''get_image_name will return the image name for a manifest. The user
       can name based on a hash or commit, or a name with the collection,
       namespace, branch, and tag.

       Parameters
       ==========
       manifest: the manifest obtained from Singularity Hub
       extension: the image extension to use (default is .simg)
       use_commit: boolean to indicate naming based on commit
       use_hash: boolean to indicate naming based on file hash

    '''
    if use_hash:
        image_name = "%s.%s" %(manifest['version'], extension)

    elif use_commit:
        image_name = "%s.%s" %(manifest['commit'], extension)

    else:
        image_name = "%s-%s-%s.%s" %(manifest['name'].replace('/','-'),
                                     manifest['branch'].replace('/','-'),
                                     manifest['tag'].replace('/',''),
                                     extension)
            
    bot.info("Singularity Registry Image: %s" %image_name)
    return image_name
