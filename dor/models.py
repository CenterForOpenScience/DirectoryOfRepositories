from django.db import models
from django import forms
import datetime
from rest_framework import fields
from treebeard.ns_tree import NS_Node


class Taxonomy(NS_Node):
    name = models.CharField(max_length=100, default='')
    tax_id = models.IntegerField(null=True, blank=True)

    node_order_by = ['tax_id', 'name']

    def __str__(self):
        if not self.is_root():
            return '{0} - {1}'.format(self.get_parent().name, self.name)
        else:
            return 'Subject: {0}'.format(self.name)

class Standards(NS_Node):
    name = models.CharField(max_length=100, default='')

    node_order_by = ['name']

    def __str__(self):
        if not self.is_root():
            return '{0} - {1}'.format(self.get_parent().name, self.name)
        else:
            return 'Standard: {0}'.format(self.name)


class ContentType(NS_Node):
    name = models.CharField(max_length=100, default='')

    node_order_by = ['name']

    def __str__(self):
        return '{0}'.format(self.name)


class Repository(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    url = models.URLField()
    accepted_taxonomy = models.ManyToManyField('Taxonomy')
    content_accepted = models.ManyToManyField('ContentType')
    standards = models.ManyToManyField('Standards')
    journals_recommend = models.TextField(default='')
    description = models.TextField(blank=True, default='')
    hosting_institution = models.CharField(max_length=100, blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='repodir')
    contact = models.CharField(max_length=100, blank=True, default='')
    metadata = models.TextField(default='')
    size = models.IntegerField(default=0)
    date_operational = models.DateField(default=datetime.date(1900, 1, 1))
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    
    class Meta:
        ordering = ('created',)

    def save(self, *args, **kwargs):
        super(Repository, self).save(*args, **kwargs)

