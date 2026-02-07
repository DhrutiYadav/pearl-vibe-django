from django import template
import re
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def highlight(text, search):
    if not text or not search:
        return text

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    highlighted = pattern.sub(
        lambda match: f"<mark>{match.group(0)}</mark>", text
    )
    return mark_safe(highlighted)
