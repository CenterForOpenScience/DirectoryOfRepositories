from django import forms
from django.utils.safestring import mark_safe


class NestedCheckboxSelectMultiple(forms.widgets.CheckboxSelectMultiple):

    def render(self, name, value, attrs=None, choices=()):
        #import ipdb
        #tree_data = []
        #for choice in self.choices.queryset:
        #    tree_item = {}
        #    tree_item['id'] = choice.id
        #    tree_item['parent'] = choice.parent or '#'
        #    tree_item['text'] = choice.obj_name
        #    tree_item['icon'] = False
        #    tree_item['state'] = {}
        #    if not choice.parent:
        #        tree_item['state']['opened'] = True
        #    if choice.id in value:
        #        tree_item['state']['selected'] = True
        #    tree_data.append(tree_item)

        #output = '<script>$(\"#{1}-container\").jstree({\"plugins\": [\"wholerow\", \"checkbox\"],\"core\":{\"data\": {0} }});</script><div id=\"{1}-container\" class=\"jstree jstree-default jstree-checkbox-selection\" role=\"tree\" aria-multiselectable=\"true\"></div>'.format(tree_data, name)
        #ipdb.set_trace()

        out = '<div style="border: solid 1px #CCC; height: 200px; overflow: auto; float: left">{}</div>'.format(super(NestedCheckboxSelectMultiple, self).render(name, value, attrs=attrs, choices=choices))
        return mark_safe(out)
