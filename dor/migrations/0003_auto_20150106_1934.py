# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dor', '0002_auto_20150106_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='plaintext_taxonomies',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
