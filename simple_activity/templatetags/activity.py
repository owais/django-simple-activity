from django import template
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType


register = template.Library()


@register.assignment_tag
def has_unread_events(object, unread_events):
    content_type = ContentType.objects.get_for_model(object)

    obj_list = [event for event in unread_events.get(content_type.id, []) if event.object_id == object.id]
    if obj_list:
        return obj_list
    else:
        return []


@register.simple_tag(takes_context=True)
def render_action(context, action):
    context['action'] = action
    return render_to_string(action.verb_object.template_name, context)
