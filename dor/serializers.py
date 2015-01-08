#from django.forms import widgets
from rest_framework import serializers
from dor.models import Repository, Taxonomy, Standards, ContentType
from django.contrib.auth.models import User
from rest_framework import fields as rest_fields

class TaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxonomy
        fields = ('name', 'tax_id',)
        depth = 3


class StandardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Standards
        fields = ('name',)
        depth = 1


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ('name',)
        depth = 2
        

class RepositorySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Repository
        fields = ('name', 'url', 'accepted_taxonomy', 'standards', 'content_accepted',
                  'journals_recommend', 'description', 'hosting_institution',
                  'owner', 'contact', 'metadata', 'size', 'date_operational',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    repos = serializers.HyperlinkedRelatedField(many=True, view_name='repository-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'repos')
