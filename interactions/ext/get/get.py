from typing import List, Type, TypeVar, Union, _GenericAlias, get_args

from ..api.models.channel import Channel
from ..api.models.guild import Guild
from ..api.models.message import Emoji
from ..api.models.role import Role
from .bot import Client

_T = TypeVar("_T")


async def get(
    client: Client, obj: Union[Type[_T], Type[List[_T]]], **kwargs
) -> Union[_T, List[_T]]:
    r"""
    A helper method for retrieving data from the Discord API in its object representation.

    :param client: Your instance of `interactions.Client`
    :type client: Client
    :param obj: The object to get. Should be a class object (not an instance!). For example: `interactions.Channel`.
    :type obj: Union[Type[_T], Type[List[_T]]
    :param \**kwargs: The arguments to pass to the HTTP method.
    :type \**kwargs: dict
    :return: The object we're trying to get.
    :rtype: Union[_T, List[_T]]
    """

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
