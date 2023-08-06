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
from sregistry.auth import (
    read_client_secrets,
    update_client_secrets
)
from sregistry.main import ApiConnection
from globus_sdk import TransferAPIError
import globus_sdk
import json
import sys
import os

from .auth import authorize
from .pull import pull
from .push import push
from .delete import remove
from .query import *

class Client(ApiConnection):

    def __init__(self, secrets=None, base=None, **kwargs):
 
        self.client = None
        self._client_id = "ae32247c-2c17-4c43-92b5-ba7fe9957dbb"        
        self._update_secrets()
        super(ApiConnection, self).__init__(**kwargs)


    def __str__(self):
        return "globus.client.%s" %(self.base)


    def _update_secrets(self):
        '''after we retrieve response with tokens, update the client secrets
           file
        '''
        if self.response is None:
            self._init_clients()

        updates = {'auth': self.response['auth'],
                   'transfer': self.response['transfer']}

        update_client_secrets(backend='globus',
                              updates=updates)

    def get_base_client(self, reset=False):
        '''the base client has entrypoints for getting a transfer or 
           authentication client, starting with a token for the app
        '''
        if self.client is None or reset is True:
            self.client = globus_sdk.NativeAppAuthClient(self._client_id)
            self.client.oauth2_start_flow()
        return self.client      


    def get_transfer_client(self):
        '''return a transfer client for the user
        ''' 
        if not hasattr(self, 'transfer'):
            self.transfer = self._init_clients()

        transfer_token = self.transfer['access_token']
        authorizer = globus_sdk.AccessTokenAuthorizer(transfer_token)
        self.transfer_client = globus_sdk.TransferClient(authorizer=authorizer)
        return self.transfer_client


    def _init_clients(self):
        '''redo the authentication flow with a code, and then tokens.
           Taken almost verbatim from:

           http://globus-sdk-python.readthedocs.io/en/stable/...
                  tutorial/#step-2-get-and-save-client-id
        '''

        # Step 1: open browser and authenticate
        self.client = self.get_base_client()

        self.client = globus_sdk.NativeAppAuthClient(self._client_id)
        self.client.oauth2_start_flow()

        url = self.client.oauth2_get_authorize_url()
        print('Please go to this URL and login: %s' %url)

        # Step 2: Get codes for client
        get_input = getattr(__builtins__, 'raw_input', input)
        message = 'Please enter the code you get after login here: '
        auth_code = get_input(message).strip()

        # Step 3: Exchange code for tokens
        self.response = self.client.oauth2_exchange_code_for_tokens(auth_code)
        self.auth = self.response.by_resource_server['auth.globus.org']
        self.transfer = self.response.by_resource_server['transfer.api.globus.org']


    def ls_endpoints(self, quiet=False):
        '''use a transfer client to list endpoints for the user.
           the intention here would be to return a list to the user for him/her
           to select from for "get"
        '''
        if not hasattr(self, 'transfer_client'):
            self.get_transfer_client()

        count = 1
        self.endpoints = []
        for scope in ['my-endpoints', 'shared-with-me']:
            for ep in self.transfer_client.endpoint_search(filter_scope=scope):
                self.endpoints.append(ep.__dict__['_data'])
                if quiet is False:

                    # Information we want to show the user
                    ep_name = ep.__dict__['_data']['display_name']
                    ep_id = ep.__dict__['_data']['id']
                    ep_owner = ep.__dict__['_data']['owner_string']

                    # Print tabular
                    bot.custom(prefix="%s %s" %(count, ep_name), color="CYAN")
                    print("%s\n%s\n%s\n" %(ep_name, ep_id, ep_owner))
                    count+=1

        return self.endpoints


    def ls_containers(self, endpoint_id):
        '''get a particular endpoint container list for a user based on 
           an endpoint ID, meaning 
           the list of singularity images included. This also
           will initialize a singularity registry directory structure
        '''
        try:
            client = get_transfer_client()
            containers = client.operation_ls(endpoint_id)
        except TransferAPIError:
            bot.error('Endpoint connection failed.')

        tdata = globus_sdk.TransferData(client, source_endpoint,
                                        endpoint,
                                        label="Singularity Registry Transfer",
                                        sync_level="checksum")


    def do_transfer(user, endpoint, container):

        # Use relative paths, we are in container and endpoint is mapped
        source = container.get_image_path().replace(settings.MEDIA_ROOT,'').strip('/')    
        client = get_transfer_client(user)
        source_endpoint = settings.GLOBUS_ENDPOINT_ID
        tdata = globus_sdk.TransferData(client, source_endpoint,
                                        endpoint,
                                        label="Singularity Registry Transfer",
                                        sync_level="checksum")
        tdata.add_item(source, source)
        transfer_result = client.submit_transfer(tdata)
        return transfer_result

    # TODO:
    # 1. write function to connect to an endpoint. 
    # 2. initialize the endpoint with a base structure, if doesn't exist
    # 3. write functions to save, pull, list, etc, based on endpoint.


def associate_user(user, client, code):
    ''' Here we do the following:

    1. Find the user's Globus account based on email. If the
       association doesn't exist, we create it.
    2. Update the token infos. We just save as extra data.
    '''

    # Second step, get tokens from code
    tokens = client.oauth2_exchange_code_for_tokens(code)

    # Associate with the user account
    token_id = tokens.decode_id_token(client)
 
    # Look up the user based on email
    email = token_id['email']
    try:
        social = user.social_auth.get(provider="globus",
                                      uid=token_id["sub"])

    except UserSocialAuth.DoesNotExist:
        social = UserSocialAuth.objects.create(provider="globus",
                                               user=user,
                                               uid=token_id["sub"])  

    # Update with token_id infos
    social.extra_data = list_tokens(tokens.data)
    social.save()  
    return user


    def logout(self):
        '''log the user out of globus, meaning deleting the association,
        and then revoking all tokens
        '''
        credentials = request.user.disconnect('globus')
        client = get_client()
        for resource, token_info in credentials.extra_data.items(): 
            for token, token_type in token_info.items():
                client.oauth2_revoke_token(
                    token, additional_params={'token_type_hint': token_type})

        # Redirect to globus logout page?
        redirect_name = "Singularity Registry"
        redirect_url = "%s%s" %(settings.DOMAIN_NAME, reverse('profile'))
        logout_url = 'https://auth.globus.org/v2/web/logout'
        params = '?client=%s&redirect_uri=%s&redirect_name=%s' %(client._client_id,
                                                                 redirect_url,
                                                                 redirect_name)
        return redirect("%s%s" %(logout_url, params))


    def globus_login(self):
        '''
          Associate the logged in user with a globus account based on email.
          If the association doesn't exist, create it. Redirect to transfer
          page.
        '''
        # redirect_uri = reverse('globus_login')
        redirect_uri = "http://localhost/globus/login/"

        client = get_client()
        client.oauth2_start_flow(redirect_uri,
                                 refresh_tokens=True)

        # First step of authentication flow - we need code
        if "code" not in request.GET:
            auth_uri = client.oauth2_get_authorize_url()
            return redirect(auth_uri)

        else:

            # Second step of authentication flow - we need to ask for token  
            code = request.GET.get('code')
            user = associate_user(request.user, 
                                  client=client, 
                                  code=code)

        return redirect('globus_transfer')


def globus_transfer(request, cid=None):
    ''' a main portal for working with globus. If the user has navigated
        here with a container id, it is presented with option to do a 
        transfer
    '''
    container = None
    if cid is not None:
        container = get_container(cid)
    endpoints = get_endpoints(request.user)
    context = {'user': request.user,
               'endpoints': endpoints,
               'container': container }

    return render(request, 'globus/transfer.html', context)


def submit_transfer(request, endpoint, cid):
    '''submit a transfer request for a container id to an endpoint, also
       based on id
    '''

    container = get_container(cid)
    if container is None:
        message = "This container could not be found."

    else:
        result = do_transfer(user=request.user,
                             endpoint=endpoint,
                             container=container)
        message = result['message']

    status = {'message': message }
    return JsonResponse(status)



#Client.authorize = authorize
#Client.ls = ls
#Client.remove = remove
#Client.pull = pull
#Client.push = push
#Client.search = search
#Client.collection_search = collection_search
#Client.container_search = container_search
#Client.label_search = label_search
