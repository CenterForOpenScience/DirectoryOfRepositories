from django import forms
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from itertools import chain


class NestedCheckboxSelectMultiple(forms.widgets.CheckboxSelectMultiple):

    items_per_row = 1  # Number of items per row

    def __init__(self, *args, **kwargs):
        super(NestedCheckboxSelectMultiple, self).__init__(*args, **kwargs)

    #def render(self, *args, **kwargs):
        #out = super(NestedCheckboxSelectMultiple, self).render(*args, **kwargs)
        #out = '<div style="width:auto;height:300px;overflow:scroll;">\n' + out + '</div>'
        #tmp = out.splitlines()
        #out = out.splitlines()
        #for line in tmp:
        #    #import ipdb; ipdb.set_trace()
        #    if(re.search('root: ', line)):
        #        out.insert(out.index(line) + 1, '<ul>')
        #        if(tmp.index(line) > 2):
        #            out.insert(out.index(line), '</ul>')
        #out.append('</ul>')
        #rv = ''.join(line for line in out)
        #return mark_safe(u''.join(rv))

    def render(self, name, value, attrs=None, choices=()):
        import ipdb
        if value is None:
            value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = ['<table><tr>']
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
        #ipdb.set_trace()
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = ' for="%s"' % final_attrs['id']
            else:
                #ipdb.set_trace()
                label_for = ''           
                cb = forms.CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
                option_value = force_unicode(option_value)
                rendered_cb = cb.render(name, option_value)
                ipdb.set_trace()
                option_label = conditional_escape(force_unicode(option_label))
            if i != 0 and i % self.items_per_row == 0:
                output.append('</tr><tr>')
            #Here you need to put you layout logic for display the checkboxes 
            if label_for:
                output.append('<td nowrap><label%s>%s</label></td>' % (label_for, option_label))
            else:
                output.append('<td nowrap><label%s>%s %s</label></td>' % (label_for, rendered_cb, option_label))

        output.append('</tr></table>')   
        ipdb.set_trace()   
        return mark_safe('\n'.join(output))
