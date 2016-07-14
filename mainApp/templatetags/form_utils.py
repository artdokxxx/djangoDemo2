from django.template import Library
register = Library()


@register.filter(name='add_class')
def add_class(field, class_name):
    return field.as_widget(attrs={
        "class": " ".join((field.css_classes(), class_name))
    })


@register.filter(name='label_add_class', is_safe=True)
def label_add_class(value, arg):
    return value.label_tag(attrs={'class': arg})