from itertools import chain
import re
from django import forms
from django.db import models
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.encoding import force_text
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

class NestedCheckboxSelectMultiple(forms.CheckboxSelectMultiple):

    items_per_row = 1 # Number of items per row  

    def __init__(self, *args, **kwargs):
        super(NestedCheckboxSelectMultiple, self).__init__(*args, **kwargs)
        #self.value = force_text(self.value) 

    def render(self, *args, **kwargs):
        out = super(NestedCheckboxSelectMultiple, self).render(*args, **kwargs)
        out = '<div style="width:auto;height:300px;overflow:scroll;">\n' + out + '</div>'
        tmp = out.splitlines()
        out = out.splitlines()
        for line in tmp: 
            if(re.search('root: ', line)):  
                out.insert(out.index(line) + 1, '<ul>')
                if(tmp.index(line) > 2): 
                    out.insert(out.index(line), '</ul>')
        out.append('</ul>')
        rv = ''.join(line for line in out)  
        return rv


