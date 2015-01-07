from django.db import models
from django import forms
from dor.index_terms import INDEX_TERMS
import datetime
from rest_framework import fields
from treebeard.ns_tree import NS_Node

TAXONOMY_CHOICES = sorted([(int(subj.split(' ')[0]), tax + "- " + subj)
                            for tax in INDEX_TERMS
                                for subj in INDEX_TERMS[tax]])
TAXONOMY_DICT = dict(TAXONOMY_CHOICES)

class Taxonomy(NS_Node):
    name = models.CharField(max_length=50)
    tax_id = models.IntegerField(null=True, blank=True)

    node_order_by = ['name', 'tax_id']


class Repository(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    url = models.URLField()
    accepted_taxonomy = models.CommaSeparatedIntegerField(max_length=len(TAXONOMY_CHOICES), choices=TAXONOMY_CHOICES, null=True, blank=True)
    datatypes_accepted = models.TextField(default='')
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
        #Build taxonomy tree here
        super(Repository, self).save(*args, **kwargs)

    def display_taxonomies(self, *args, **kwargs):
        rv = ''
        for index in self.accepted_taxonomy:
            rv += TAXONOMY_DICT[index] + ' \n'
        return rv
