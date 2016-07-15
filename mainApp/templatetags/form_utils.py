from django.template import Library
from django.forms.fields import CheckboxInput
register = Library()


@register.filter(name='add_class')
def add_class(field, class_name):
    return field.as_widget(attrs={
        "class": " ".join((field.css_classes(), class_name))
    })


@register.filter(name='label_add_class', is_safe=True)
def label_add_class(value, arg):
    return value.label_tag(attrs={'class': arg})


@register.filter(name='is_checkbox')
def is_checkbox(value):
    return isinstance(value, CheckboxInput)


@register.simple_tag
def active_page(request, view_name):
    from django.core.urlresolvers import resolve, Resolver404
    if not request:
        return ""
    try:
        return "active" if resolve(request.path_info).url_name == view_name else ""
    except Resolver404:
        return ""