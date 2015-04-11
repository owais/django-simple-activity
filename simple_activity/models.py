from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from filtered_contenttypes.fields import FilteredGenericForeignKey
from django_pgjson.fields import JsonBField

from .managers import ActionManager
from . import registry
from . import settings


def _default_action_meta():
    return {}


class BaseAction(models.Model):
    item_type = models.ForeignKey(ContentType, related_name='actions')
    item_id = models.PositiveIntegerField()
    item = FilteredGenericForeignKey('item_type', 'item_id')

    target_type = models.ForeignKey(ContentType, blank=True, null=True,
                                    related_name='target_actions')
    target_id = models.PositiveIntegerField(blank=True, null=True)
    target = FilteredGenericForeignKey('target_type', 'target_id')

    actor = models.ForeignKey('users.User', related_name='activity')
    verb = models.CharField(max_length=23,
                            choices=registry.as_model_choices())
    published = models.DateTimeField(auto_now_add=True)

    meta = JsonBField(default=_default_action_meta, blank=True)

    class Meta:
        abstract = True
        ordering = ('-published',)

    @classmethod
    def add_action(klass, verb, actor, item, target=None, published=None,
                      meta={}):
        if not registry.is_valid(verb):
            raise ValueError('`{}` not a valid verb.'.format(verb))
        published = published or now()
        create_kwargs = {'actor': actor, 'item': item, 'verb': verb.code}
        if target:
            create_kwargs['target'] = target
            create_kwargs['published'] = published
        klass.objects.create(**create_kwargs)

    @property
    def verb_object(self):
        return registry.get_from_code(self.verb)


class Action(BaseAction):
    CLIENTS = 1
    VENDORS = 2
    ALL = 3
    visibility_choices = (
        (CLIENTS, 'Client'),
        (VENDORS, 'Vendors'),
        (ALL, 'Both vendors and client'),
    )

    visibility = models.PositiveIntegerField(
        default=ALL, choices=visibility_choices)

    objects = ActionManager()

    class Meta:
        abstract = settings.get('ACTION_MODEL') != 'simple_activity.Action'
        ordering = ('-published',)
