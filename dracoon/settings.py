"""
Async DRACOON settings adapter based on httpx and pydantic
V1.0.0
(c) Octavio Simone, November 2021 

Collection of DRACOON API calls for settings (Webhooks)
Documentation: https://dracoon.team/api/swagger-ui/index.html?configUrl=/api/spec_v4/swagger-config#/groups
Webhooks documentation: https://support.dracoon.com/hc/de/articles/360013167959-Webhooks 
Please note: maximum 500 items are returned in GET requests
 - refer to documentation for details on filtering and offset
 - use documentation for payload description

"""

from typing import List
import httpx
from pydantic import validate_arguments

from .core import DRACOONClient, OAuth2ConnectionType
from .settings_models import CreateWebhook, UpdateSettings, UpdateWebhook

class DRACOONSettings:

    """
    API wrapper for DRACOON settings endpoint:
    Settings an webhooks management – config manager role required
    """
    
    def __init__(self, dracoon_client: DRACOONClient):
        """ requires a DRACOONClient to perform any request """
        if not isinstance(dracoon_client, DRACOONClient):
            raise TypeError('Invalid DRACOON client format.')
        if dracoon_client.connection:
           self.dracoon = dracoon_client
           self.api_url = self.dracoon.base_url + self.dracoon.api_base_url + '/settings'
        else:
            raise ValueError('DRACOON client must be connected: client.connect()')

    @validate_arguments
    async def get_settings(self):
        """ list customer settings (home rooms) """
        if not await self.dracoon.test_connection() and self.dracoon.connection:
            await self.dracoon.connect(OAuth2ConnectionType.refresh_token)
        try:
            res = await self.dracoon.http.get(self.api_url)
            print(res)

        except httpx.RequestError as e:
            raise httpx.RequestError(f'Connection to DRACOON failed: {e.request.url}')

        return res

    @validate_arguments
    async def update_settings(self, settings_update: UpdateSettings):
        """ update customer settings (home rooms) """
        if not await self.dracoon.test_connection() and self.dracoon.connection:
            await self.dracoon.connect(OAuth2ConnectionType.refresh_token)

        payload = settings_update.dict(exclude_unset=True)

        try:
            res = await self.dracoon.http.put(url=self.pi_url, json=payload)

        except httpx.RequestError as e:
            raise httpx.RequestError(f'Connection to DRACOON failed: {e.request.url}')

        return res
    
    def make_settings_update(self, home_rooms_active: bool = None, home_room_quota: int = None, home_room_parent_name: str = None) -> UpdateSettings:
        """ make a settings update payload required for update_settings() """
        settings_update = {}

        if home_rooms_active == False:
            raise ValueError('Home rooms cannot be deactivated')

        if home_rooms_active: settings_update["homeRoomsActive"] = home_rooms_active
        if home_room_quota: settings_update["homeRoomQuota"] = home_room_quota
        if home_room_parent_name: settings_update["homeRoomParentName"] = home_room_parent_name

        return settings_update

    @validate_arguments
    async def get_webhooks(self, offset: int = 0, filter: str = None, limit: int = None, sort: str = None):
        """ list (all) webhooks """
        if not await self.dracoon.test_connection() and self.dracoon.connection:
            await self.dracoon.connect(OAuth2ConnectionType.refresh_token)

        api_url = self.api_url + f'/webhooks/?offset={offset}'
        if filter != None: api_url += f'&filter={filter}' 
        if limit != None: api_url += f'&limit={str(limit)}' 
        if sort != None: api_url += f'&sort={sort}' 

        try:
            res = await self.dracoon.http.get(api_url)
            print(res)

        except httpx.RequestError as e:
            raise httpx.RequestError(f'Connection to DRACOON failed: {e.request.url}')

        return res


    @validate_arguments
    async def create_webhook(self, user: CreateWebhook):
        """ creates a new webhook """
        payload = user.dict(exclude_unset=True)

        if not await self.dracoon.test_connection() and self.dracoon.connection:
            await self.dracoon.connect(OAuth2ConnectionType.refresh_token)

        api_url = self.api_url + f'/webhooks'
        try:
            res = await self.dracoon.http.post(api_url, json=payload)

        except httpx.RequestError as e:
            raise httpx.RequestError(f'Connection to DRACOON failed: {e.request.url}')

        return res

    def make_webhook(self, name: str, event_types: List[str], url: str, secret: str = None, 
                     is_enabled: bool = None, trigger_example: bool = None) -> CreateWebhook:
        """ make a new webhook creation payload required for create_webhook() """
        webhook = {
            "name": name,
            "eventTypeNames": event_types,
            "url": url
        }
        
        if secret: webhook["secret"] = secret
        if is_enabled is not None: webhook["isEnabled"] = is_enabled
        if trigger_example is not None: webhook["triggerExampleEvent"] = trigger_example

        return webhook

    def make_webhook_update(self, name: str = None, event_types: List[str] = None, url: str = None, secret: str = None, 
                     is_enabled: bool = None, trigger_example: bool = None) -> CreateWebhook:
        """ make a new webhook update payload required for update_webhook() """
        webhook = {}
        
        if name: webhook["name"] = name
        if event_types: webhook["eventTypeNames"] = event_types
        if url: webhook["url"] = url
        if secret: webhook["secret"] = secret
        if is_enabled is not None: webhook["isEnabled"] = is_enabled
        if trigger_example is not None: webhook["triggerExampleEvent"] = trigger_example

        return webhook


    # get user details for given user id
    @validate_arguments
    async def get_webhook(self, hook_id: int):
        """ get webhook details for specific user (by id) """
        if not await self.dracoon.test_connection() and self.dracoon.connection:
            await self.dracoon.connect(OAuth2ConnectionType.refresh_token)

        api_url = self.api_url + f'/webhooks/{str(hook_id)}'

        try:
            res = await self.dracoon.http.get(api_url)

        except httpx.RequestError as e:
            raise httpx.RequestError(f'Connection to DRACOON failed: {e.request.url}')

        return res

    @validate_arguments
    async def update_webhook(self, hook_id: int, hook_update: UpdateWebhook):

        payload = hook_update.dict(exclude_unset=True)

        if not await self.dracoon.test_connection() and self.dracoon.connection:
            await self.dracoon.connect(OAuth2ConnectionType.refresh_token)

        api_url = self.api_url + f'/webhooks/{str(hook_id)}'

        try:
            res = await self.dracoon.http.put(api_url, json=payload)

        except httpx.RequestError as e:
            raise httpx.RequestError(f'Connection to DRACOON failed: {e.request.url}')

        return res

    # delete user for given user id
    @validate_arguments
    async def delete_webhook(self, hook_id: int):
        if not await self.dracoon.test_connection() and self.dracoon.connection:
            await self.dracoon.connect(OAuth2ConnectionType.refresh_token)

        api_url = self.api_url + f'/webhooks/{str(hook_id)}'

        try:
            res = await self.dracoon.http.delete(api_url)

        except httpx.RequestError as e:
            raise httpx.RequestError(f'Connection to DRACOON failed: {e.request.url}')

        return res
    
    # get user details for given user id
    @validate_arguments
    async def get_webhook_event_types(self):

        if not await self.dracoon.test_connection() and self.dracoon.connection:
            await self.dracoon.connect(OAuth2ConnectionType.refresh_token)

        api_url = self.api_url + f'/webhooks/event_types'

        try:
            res = await self.dracoon.http.get(api_url)

        except httpx.RequestError as e:
            raise httpx.RequestError(f'Connection to DRACOON failed: {e.request.url}')

        return res


"""
LEGACY API (0.4.x) - DO NOT MODIFY

"""

# get customer settings
def get_settings():
    api_call = {
            'url': '/settings',
            'body': None,
            'method': 'GET',
            'content_type': 'application/json'
        }
    return api_call

# get customer settings
@validate_arguments
def update_settings(params: UpdateSettings):
    api_call = {
            'url': '/settings',
            'body': params,
            'method': 'PUT',
            'content_type': 'application/json'
        }
    return api_call

# get customer webhooks 
@validate_arguments
def get_webhooks(offset: int = 0, filter: str = None, limit: int = None, sort: str = None):
    api_call = {
            'url': '/settings/webhooks?offset=' + str(offset),
            'body': None,
            'method': 'GET',
            'content_type': 'application/json'
        }
        
    if filter != None: api_call['url'] += '&filter=' + filter
    if limit != None: api_call['url'] += '&limit=' + str(limit)
    if sort != None: api_call['url'] += '&sort=' + sort

    return api_call

# create a webhook with given parameters - please refer to documentation above
@validate_arguments
def create_webhook(params: CreateWebhook):
    api_call = {
        'url': '/settings/webhooks',
        'body': params,
        'method': 'POST',
        'content_type': 'application/json'
    }
    return api_call

# get webhook details for given hook id
@validate_arguments
def get_webhook(hookID: int):
    api_call = {
        'url': '/settings/webhooks/' + str(hookID),
        'body': None,
        'method': 'GET',
        'content_type': 'application/json'
    }
    return api_call

# update webhook data for given hook id
@validate_arguments
def update_webhook(hookID: int, params: UpdateWebhook):
    api_call = {
        'url': '/settings/webhooks/' + str(hookID),
        'body': params,
        'method': 'PUT',
        'content_type': 'application/json'
    }
    return api_call

# delete webhook for given hook id
@validate_arguments
def delete_webhook(hookID: int):
    api_call = {
        'url': '/settings/webhooks/' + str(hookID),
        'body': None,
        'method': 'DELETE',
        'content_type': 'application/json'
    }
    return api_call

# get webhook event types
def get_hook_event_types():
    api_call = {
            'url': '/settings/webhooks/event_types',
            'body': None,
            'method': 'GET',
            'content_type': 'application/json'
        }
    return api_call