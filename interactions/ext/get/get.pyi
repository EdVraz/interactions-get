from typing import overload, Type, TypeVar, List

from .bot import Client

from ..api.models.channel import Channel
from ..api.models.guild import Guild
from ..api.models.member import Member
from ..api.models.message import Message, Emoji, Sticker
from ..api.models.role import Role
from ..api.models.user import User
from ..api.models.webhook import Webhook

_T = TypeVar("_T")

# single objects
@overload
async def get(client: Client, obj: Type[Channel], *, channel_id: int) -> Channel: ...
@overload
async def get(client: Client, obj: Type[Emoji], *, guild_id: int, emoji_id: int) -> Emoji: ...
@overload
async def get(client: Client, obj: Type[Guild], *, guild_id: int) -> Guild: ...
@overload
async def get(client: Client, obj: Type[Member], *, guild_id: int, member_id: int) -> Member: ...
@overload
async def get(
    client: Client,
    obj: Type[Message],
    *,
    channel_id: int,
    message_id: int,
) -> Message: ...
@overload
async def get(client: Client, obj: Type[Role], *, guild_id: int, role_id: int) -> Role: ...
@overload
async def get(client: Client, obj: Type[Sticker], *, sticker_id: int) -> Sticker: ...
@overload
async def get(client: Client, obj: Type[User], *, user_id: int) -> User: ...
@overload
async def get(client: Client, obj: Type[Webhook], *, webhook_id: int) -> Webhook: ...
# list of objects
@overload
async def get(client: Client, obj: Type[List[Channel]], *, channel_ids: List[int]) -> List[Channel]: ...
@overload
async def get(client: Client, obj: Type[List[Emoji]], *, guild_id: int, emoji_ids: List[int]) -> List[Emoji]: ...
@overload
async def get(client: Client, obj: Type[List[Guild]], *, guild_ids: List[int]) -> List[Guild]: ...
@overload
async def get(client: Client, obj: Type[List[Member]], *, guild_id: int, member_ids: List[int]) -> List[Member]: ...
@overload
async def get(
    client: Client,
    obj: Type[List[Message]],
    *,
    channel_id: int,
    message_ids: List[int],
) -> List[Message]: ...
@overload
async def get(client: Client, obj: Type[List[Role]], *, guild_id: int, role_ids: List[int]) -> List[Role]: ...
@overload
async def get(client: Client, obj: Type[List[Sticker]], *, sticker_ids: List[int]) -> List[Sticker]: ...
@overload
async def get(client: Client, obj: Type[List[User]], *, user_ids: List[int]) -> List[User]: ...
@overload
async def get(client: Client, obj: Type[List[Webhook]], *, webhook_ids: List[int]) -> List[Webhook]: ...
# Having a not-overloaded definition stops showing a warning/complaint from the IDE if wrong arguments are put in,
# so we'll leave that out
