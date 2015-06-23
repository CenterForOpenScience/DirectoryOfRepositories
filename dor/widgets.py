import re
from django.forms import widgets
from django.utils.safestring import mark_safe


class NestedCheckboxSelectMultiple(widgets.CheckboxSelectMultiple):

    items_per_row = 1  # Number of items per row

    def __init__(self, *args, **kwargs):
        super(NestedCheckboxSelectMultiple, self).__init__(*args, **kwargs)

    def render(self, *args, **kwargs):
        out = super(NestedCheckboxSelectMultiple, self).render(*args, **kwargs)
        out = '<div style="width:auto;height:300px;overflow:scroll;">\n' + out + '</div>'
        tmp = out.splitlines()
        out = out.splitlines()
        for line in tmp:
            #import ipdb; ipdb.set_trace()
            if(re.search('root: ', line)):
                out.insert(out.index(line) + 1, '<ul>')
                if(tmp.index(line) > 2):
                    out.insert(out.index(line), '</ul>')
        out.append('</ul>')
        rv = ''.join(line for line in out)
        return mark_safe(u''.join(rv))
