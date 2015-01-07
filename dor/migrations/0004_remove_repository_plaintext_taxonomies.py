# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dor', '0003_auto_20150106_1934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repository',
            name='plaintext_taxonomies',
        ),
    ]
