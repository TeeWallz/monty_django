from django import template
from django.utils.html import escape, mark_safe
from guestbook.constants import SMILIES_MAP
import re

register = template.Library()

_SMILIES_RE = re.compile("|".join(map(re.escape, SMILIES_MAP.keys())))


@register.filter(name="render_smilies")
def render_smilies(value):
    text = escape(value)
    result = _SMILIES_RE.sub(
        lambda match: f'<img src="{SMILIES_MAP[match.group(0)]}" alt="">',
        text,
    )
    return mark_safe(result)
