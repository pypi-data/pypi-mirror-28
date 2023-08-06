# py-front

A python API wrapper around [Front](https://frontapp.com).

# Installation

```bash
pip install py-front
```

# Usage

## Set api key

```python
import front
front.set_api_key("jwt_token")
```

## Use the api

```python
import front

for conv in front.Conversation.objects.all():
    print(conv.id, conv.subject)
```

# Available models

- Contact
  - https://dev.frontapp.com/#contacts
- Tag
  - https://dev.frontapp.com/#tags
- Channel
  - https://dev.frontapp.com/#channels
- Conversation
  - https://dev.frontapp.com/#conversations
- Inbox
  - https://dev.frontapp.com/#inboxes
- Teammate
  - https://dev.frontapp.com/#teammates
- _More soon..._ PRs are welcome!
