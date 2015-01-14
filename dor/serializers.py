#from django.forms import widgets
from rest_framework import serializers
from dor.models import Repository, Taxonomy, Standards,\
    ContentType, Journal
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username',)


class JournalSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Journal
        fields = ('name', 'repos_endorsed', 'owner')

class TaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxonomy
        fields = ('name', 'tax_id',)


class StandardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Standards
        fields = ('name',)


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ('name',)


class RepositorySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Repository
        fields = ('name', 'url', 'accepted_taxonomy', 'standards', 'owner',
                  'accepted_content', 'description', 'hosting_institution',
                  'contact', 'metadata', 'size', 'date_operational',)
