import logging

from django import template
from django.conf import settings
from django.templatetags.static import static

from cms.contexts.utils import append_slash
from cms.menus.models import NavigationBarItem


logger = logging.getLogger(__name__)
register = template.Library()


# def _get_same_level_items(item, path, language, exclude_item=True):
def _get_same_level_items(item, language, exclude_item=True):
    parent = item.parent
    # if parent:
    items = parent.get_childs(lang=language, exclude=item) \
            if exclude_item \
            else parent.get_childs(lang=language)
    return {'parent': parent.localized(lang=language),
            'items': items,
            'current': item.localized(lang=language)}
    # return {}

    # webpath = item.webpath
    # if webpath and not webpath.is_alias:
        # if path == webpath.get_full_path():
            # parent = item.parent
            ## if parent:
            # items = parent.get_childs(lang=language, exclude=item) \
                    # if exclude_item \
                    # else parent.get_childs(lang=language)
            # return {'parent': parent.localized(lang=language),
                    # 'items': items,
                    # 'current': item}
    # for child in item.get_childs():
        # result = _get_same_level_items(child, path, language,
                                       # exclude_item=exclude_item)
        # if result: return result
    # return {}


@register.simple_tag(takes_context=True)
def load_same_level_items(context, exclude_item=True):
    _func_name = 'load_same_level_items'
    _log_msg = f'Template Tag {_func_name}'

    request = context['request']
    language = getattr(request, 'LANGUAGE_CODE', '')

    # path = context['page'].webpath.get_full_path()

    item = NavigationBarItem.objects.filter(menu=context['items'][0].menu,
                                            is_active=True,
                                            webpath=context['page'].webpath,
                                            webpath__alias__isnull=True,
                                            webpath__is_active=True).first()
    if item:
        result = _get_same_level_items(item, language, exclude_item=exclude_item)
        return result


# def _get_current_item(item, path, language):
    # webpath = item.webpath
    # if webpath and not webpath.is_alias:
        # if path == webpath.get_full_path():
            # return item
    # for child in item.get_childs():
        # result = _get_current_item(child, path, language)
        # if result: return result
    # return None


@register.simple_tag(takes_context=True)
def load_current_item_from_menu(context):
    _func_name = 'load_current_item_from_menu'
    _log_msg = f'Template Tag {_func_name}'

    request = context['request']
    language = getattr(request, 'LANGUAGE_CODE', '')

    item = NavigationBarItem.objects.filter(menu=context['items'][0].menu,
                                            is_active=True,
                                            webpath=context['page'].webpath,
                                            webpath__alias__isnull=True,
                                            webpath__is_active=True).first()
    if item:
        if item.inherited_content: item.inherited_content.translate_as(language)
        if item.publication: item.publication.translate_as(language)
        return item.localized(lang=language)
    # return item if item else None

    # path = context['page'].webpath.get_full_path()

    # for item in context['items']:
        # result = _get_current_item(item, path, language)
        # if result: return result


@register.simple_tag
def load_lang_flag(lang):
    if not lang: return ''
    return static(f'/images/flags/{lang}.svg')


@register.simple_tag
def unicms_template_unical_static_path(resource):
    if not resource: return ''
    if settings.UNICMS_TEMPLATE_UNICAL_USE_CDN:
        return f'{settings.UNICMS_TEMPLATE_UNICAL_CDN}/{resource}'
    return static(resource)
