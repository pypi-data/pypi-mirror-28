import asyncio

from aiopvapi.helpers.tools import get_base_path
from aiopvapi.helpers.api_base import ApiResource
from aiopvapi.helpers.constants import ATTR_SCENE, ATTR_ROOM_ID, \
    ATTR_SCENE_ID, URL_SCENES



class Scene(ApiResource):
    def __init__(self, raw_data, hub_ip=None, loop=None, websession=None):
        if ATTR_SCENE in raw_data:
            raw_data = raw_data.get(ATTR_SCENE)
        super().__init__(loop, websession, get_base_path(hub_ip, URL_SCENES),
                         raw_data)

    @property
    def room_id(self):
        return self._raw_data.get(ATTR_ROOM_ID)

    @asyncio.coroutine
    def activate(self):
        _val = yield from self.request.get(self._base_path,
                                           params={ATTR_SCENE_ID: self._id})
        return _val
