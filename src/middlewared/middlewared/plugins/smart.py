import re

from middlewared.schema import accepts, Dict, Int, List, Str
from middlewared.validators import Email
from middlewared.service import SystemServiceService, private


class SmartService(SystemServiceService):

    class Config:
        service = "smartd"
        service_model = "smart"
        datastore_extend = "smart.smart_extend"
        datastore_prefix = "smart_"

    @private
    async def smart_extend(self, smart):
        smart["email"] = list(filter(None, re.split(r"\s+", smart["email"])))
        return smart

    @accepts(Dict(
        'smart_update',
        Int('interval'),
        Str('powermode', enum=['never', 'sleep', 'standby', 'idle']),
        Int('difference'),
        Int('informational'),
        Int('critical'),
        List('email', items=[Str('email', validators=[Email()])]),
    ))
    async def update(self, data):
        old = await self.config()

        new = old.copy()
        new.update(data)

        new["email"] = " ".join(new["email"])

        await self._update_service(old, new)

        return new
