# interactions-get
___________________
This is a temporary extension for interactions.py, until it gets its own `get` implementation. This `get`-method 
will only get objects via a HTTP call, not from cache.

## Usage
```python
from interactions.ext.get import get
import interactions

channel = await get(client, interactions.Channel, channel_id=123)
```
Currently, supported objects to get are: `Channel, Emoji, Guild, Member, Message, Role, User` and `Webhook`. 

Additionally, you can get a list of all those objects. Here's how to:
```python
from interactions.ext.get import get
import interactions
from typing import List

channels = await get(client, List[interactions.Channel], channel_ids=[123, 456, 789])
```

The `get`-Method was made with `@typing.overload` decorators for typehinting. This means that your IDE, for example 
PyCharm or VSCode, will show, or underline the function, you when you entered wrong keyword arguments for certain objects

