#from django.forms import widgets
from rest_framework import serializers
from dor.models import Repository  # , LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User
from dor.index_terms import INDEX_TERMS
from rest_framework import fields

TAXONOMY_CHOICES = sorted([(int(subj.split(' ')[0]), tax + "- " + subj)
                            for tax in INDEX_TERMS
                                for subj in INDEX_TERMS[tax]])


class RepositorySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    accepted_taxonomy = fields.MultipleChoiceField(choices=TAXONOMY_CHOICES)

    class Meta:
        model = Repository
        fields = ('name', 'url', 'accepted_taxonomy', 'datatypes_accepted',
                  'journals_recommend', 'description', 'hosting_institution',
                  'owner', 'contact', 'metadata', 'size', 'date_operational')

    def create(self, validated_data):
        rv = Repository(name=validated_data['name'],
                        url=validated_data['url'],
                        datatypes_accepted=validated_data['datatypes_accepted'],
                        journals_recommend=validated_data['journals_recommend'],
                        description=validated_data['description'],
                        hosting_institution=validated_data['hosting_institution'],
                        owner=validated_data['owner'],
                        contact=validated_data['contact'],
                        metadata=validated_data['metadata'],
                        size=validated_data['size'],
                        date_operational=validated_data['date_operational'],
                        accepted_taxonomy = validated_data['accepted_taxonomy'])
        rv.save()
        return rv


    def to_representation(self, data):
        #By default this method causes accepted_taxonomy to be cast as a string,
        #overriding fixes that
        return {
            'name': data.name,
            'url': data.url,
            'accepted_taxonomy': data.accepted_taxonomy,
            'datatypes_accepted': data.datatypes_accepted,
            'journals_recommend': data.journals_recommend,
            'description': data.description,
            'hosting_institution': data.hosting_institution,
            'owner': data.owner.username,
            'contact': data.contact,
            'metadata': data.metadata,
            'size': data.size,
            'date_operational': data.date_operational,
        }


class UserSerializer(serializers.HyperlinkedModelSerializer):
    repos = serializers.HyperlinkedRelatedField(many=True, view_name='repository-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'repos')
