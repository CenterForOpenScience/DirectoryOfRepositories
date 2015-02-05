from django.db import models
from django.shortcuts import render_to_response
import datetime
from rest_framework import fields
from treebeard.ns_tree import NS_Node
from dor.widgets import NestedCheckboxSelectMultiple


class Journal(models.Model):
    name = models.CharField(max_length=100, default='')
    owner = models.ForeignKey('auth.User', related_name='journals')
    repos_endorsed = models.ManyToManyField('Repository',)

    def __str__(self):
        return str(self.name)


class Taxonomy(NS_Node):
    name = models.CharField(max_length=100, default='')
    tax_id = models.IntegerField(null=True, blank=True)

    node_order_by = ['tax_id', 'name']

    def __str__(self):
        if not self.is_root():
            return '{0} - {1}'.format(self.get_parent().name, self.name)
        else:
            return 'root: {0}'.format(self.name)

class Standards(NS_Node):
    name = models.CharField(max_length=100, default='')

    node_order_by = ['name']

    def __str__(self):
        if not self.is_root():
            return '{0} - {1}'.format(self.get_parent().name, self.name)
        else:
            return 'root: {0}'.format(self.name)


class ContentType(NS_Node):
    name = models.CharField(max_length=100, default='')

    node_order_by = ['name']

    def __str__(self):
        return '{0}'.format(self.name)


class Repository(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    url = models.URLField()
    accepted_taxonomy = models.ManyToManyField('Taxonomy',)
    accepted_content = models.ManyToManyField('ContentType',)
    standards = models.ManyToManyField('Standards',)
    description = models.TextField(blank=True, default='')
    hosting_institution = models.CharField(max_length=100, blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='repositorys')
    contact = models.CharField(max_length=100, blank=True, default='')
    metadata = models.TextField(default='')
    size = models.IntegerField(default=0)
    date_operational = models.DateField(default=datetime.date(1900, 1, 1))
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ('date_operational',)
    
    def __str__(self):
        return str(self.name)
