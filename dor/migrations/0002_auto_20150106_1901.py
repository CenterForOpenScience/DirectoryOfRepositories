# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='plaintext_taxonomies',
            field=models.URLField(),
            preserve_default=True,
        ),
    ]
