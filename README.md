# django-simple-activity

## settings

### Models

Simple Activity ships with a `Action` model that can be used directly.


### Using custom models



### Setting up custom Action model

In `custom_app/models.py`
```
from simple_activity.models import BaseAction

class Action(BaseAction):
   # your custom fields, managers, etc here
```

In `settings.py`
```
SIMPLE_ACTIVITY = {
    'ACTION_MODEL': 'my_app.MyActionModel'
}
```
