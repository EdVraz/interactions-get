from typing import List, Type, TypeVar, Union, _GenericAlias, get_args, Iterable

from interactions.api.models.channel import Channel
from interactions.api.models.guild import Guild
from interactions.api.models.message import Emoji
from interactions.api.models.role import Role
from interactions.client.bot import Client
from logging import getLogger

log = getLogger("get")

_T = TypeVar("_T")


async def get(*args, **kwargs):
    # sourcery no-metrics
    if len(args) == 2 and any(isinstance(_, Iterable) for _ in args):
        raise TypeError("You can only use Iterables as single-argument!")

    if len(args) == 2:
        client: Client
        obj: Union[Type[_T], Type[List[_T]]]

        client, obj = args
        if not isinstance(obj, type) and not isinstance(obj, _GenericAlias):
            raise TypeError("The object must not be an instance of a class!")

        if isinstance(obj, _GenericAlias):
            _obj = get_args(obj)[0]
            _objects: List[_obj] = []
            _name = f"get_{_obj.__name__.lower()}"

            if len(list(kwargs)) == 2:
                if guild_id := kwargs.pop("guild_id", None):
                    _guild = Guild(**await client._http.get_guild(guild_id), _client=client._http)
                    _func = getattr(_guild, _name)

                elif channel_id := kwargs.pop("channel_id", None):
                    _channel = Channel(
                        **await client._http.get_channel(channel_id), _client=client._http
                    )
                    _func = getattr(_channel, _name)

            else:
                _func = getattr(client._http, _name)

            _kwarg_name = list(kwargs)[0][:-1]

            for kwarg in kwargs.get(list(kwargs)[0]):
                _kwargs = {_kwarg_name: kwarg}
                __obj = await _func(**_kwargs)

                if isinstance(__obj, dict):
                    _objects.append(_obj(**__obj, _client=client._http))
                else:
                    _objects.append(__obj)

            return _objects

        _name = f"get_{obj.__name__.lower()}"

        if obj in (Role, Emoji):
            _guild = Guild(**await client._http.get_guild(kwargs.pop("guild_id")), _client=client._http)
            _func = getattr(_guild, _name)
            return await _func(**kwargs)

        _func = getattr(client._http, _name)
        _obj = await _func(**kwargs)
        return obj(**_obj, _client=client._http)

    elif len(args) == 1:
        item: Iterable = args[0]
        if not isinstance(item, Iterable):
            raise TypeError("The specified item must be an iterable!")

        if not kwargs:
            raise ValueError("You have to specify either the name or id to search for!")

        if len(list(kwargs)) > 1:
            raise ValueError("Only one key word argument to search for is allowed!")

        _arg = str(list(kwargs)[0])

        try:
            __obj = next(_ for _ in item if str(getattr(_, _arg, None)) == str(kwargs.get(_arg)))
            return __obj
        except StopIteration:
            log.warning("Could not retrieve any matching item!")
