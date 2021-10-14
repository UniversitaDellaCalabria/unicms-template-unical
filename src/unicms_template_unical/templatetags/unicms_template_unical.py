import logging

from django import template

from cms.contexts.utils import append_slash

logger = logging.getLogger(__name__)
register = template.Library()


def _get_same_level_items(item, path, language, exclude_item=True):
    webpath = item.webpath
    if webpath and not webpath.is_alias:
        if path == webpath.get_full_path():
            parent = item.parent
            # if parent:
            items = parent.get_childs(lang=language, exclude=item) \
                    if exclude_item \
                    else parent.get_childs(lang=language)
            return {'parent': parent.localized(lang=language),
                    'items': items,
                    'current': item}
    for child in item.get_childs():
        result = _get_same_level_items(child, path, language,
                                       exclude_item=exclude_item)
        if result: return result
    return {}


@register.simple_tag(takes_context=True)
def load_same_level_items(context, exclude_item=True):
    _func_name = 'load_same_level_items'
    _log_msg = f'Template Tag {_func_name}'

    request = context['request']
    language = getattr(request, 'LANGUAGE_CODE', '')

    path = context['page'].webpath.get_full_path()

    for item in context['items']:
        result = _get_same_level_items(item, path, language,
                                       exclude_item=exclude_item)
        if result: return result


def _get_current_item(item, path, language):
    webpath = item.webpath
    if webpath and not webpath.is_alias:
        if path == webpath.get_full_path():
            return item
    for child in item.get_childs():
        result = _get_current_item(child, path, language)
        if result: return result
    return None # pragma: no cover


@register.simple_tag(takes_context=True)
def load_current_item_from_menu(context):
    _func_name = 'load_current_item_from_menu'
    _log_msg = f'Template Tag {_func_name}'

    request = context['request']
    language = getattr(request, 'LANGUAGE_CODE', '')
    path = context['page'].webpath.get_full_path()

    for item in context['items']:
        result = _get_current_item(item, path, language)
        if result: return result
