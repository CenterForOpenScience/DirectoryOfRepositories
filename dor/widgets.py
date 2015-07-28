from django import forms
from django.utils.safestring import mark_safe


class NestedCheckboxSelectMultiple(forms.widgets.CheckboxSelectMultiple):

    def render(self, name, value, attrs=None, choices=()):
        out = '<div style="border: solid 1px #CCC; height: 200px; overflow: auto; float: left">{}</div>'.format(super(NestedCheckboxSelectMultiple, self).render(name, value, attrs=attrs, choices=choices))
        return mark_safe(out)
