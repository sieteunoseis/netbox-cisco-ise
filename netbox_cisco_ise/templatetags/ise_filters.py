"""Custom template filters for netbox-cisco-ise plugin."""

import json

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def is_dict(value):
    """Check if value is a dictionary."""
    return isinstance(value, dict)


@register.filter
def is_list(value):
    """Check if value is a list."""
    return isinstance(value, list)


@register.filter
def to_json(value, indent=2):
    """Convert value to formatted JSON string."""
    try:
        return json.dumps(value, indent=indent, sort_keys=True, default=str)
    except (TypeError, ValueError):
        return str(value)


@register.filter
def json_id_safe(value):
    """Make a value safe for use as an HTML ID (for JSON copy buttons)."""
    return str(value).replace(" ", "-").replace(".", "-").lower()
