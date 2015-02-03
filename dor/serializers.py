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
    databaseAccessTypes = serializers.ChoiceField(choices=['open', 'restricted', 'closed'])
    accessTypes = serializers.MultipleChoiceField(choices=['open', 'embargoed', 'restricted', 'closed'])
    dataUploadTypes = serializers.ChoiceField(choices=['open', 'restricted', 'closed'])
    repositoryTypes = serializers.ChoiceField(choices=['disciplinary', 'institutional', 'other'])
    providerTypes = serializers.MultipleChoiceField(choices=['dataProvider', 'serviceProvider'])
    responsibilityTypes = serializers.MultipleChoiceField(choices=['funding', 'general', 'sponsoring', 'technical'])
    institutionTypes = serializers.ChoiceField(choices=['commercial', 'non-profit'])
    databaseLicenseNames = serializers.ChoiceField(choices=['Apache License 2.0', 'BSD', 'CC', 'CC0', 'Copyrights', 'ODC', 'Public Domain', 'other'])
    apiTypes = serializers.MultipleChoiceField(choices=['API', 'FTP', 'OAI-PMH', 'REST', 'SOAP', 'SPARQL', 'SWORD', 'other'])
    pidSystems = serializers.MultipleChoiceField(choices=['ARK', 'DOI', 'HDL', 'PURL', 'URN', 'other', 'none'])
    aidSystems = serializers.MultipleChoiceField(choices=['AuthorClaim', 'ISNI ORCID', 'ResearchedID', 'other', 'none'])
    enhancedPublications = serializers.ChoiceField(choices=['yes', 'no', 'unknown'])
    qualityManagement = serializers.ChoiceField(choices=['yes', 'no', 'unknown'])
    certificates = serializers.MultipleChoiceField(choices=['CLARIN Certificate B','DIN 31644', 'DINI Certificate', 'DRAMBORA', 'DSA', 'ISO 16363', 'ISO 16919', 'RatSWD', 'TRAC', 'Trusted Digital Repository', 'WDS', 'other'])
    syndicationTypes = serializers.MultipleChoiceField(choices=['ATOM', 'RSS'])
    class Meta:
        model = Standards
        fields = ('databaseAccessTypes', 'accessTypes', 'dataUploadTypes', 
                  'repositoryTypes', 'providerTypes', 'enhancedPublications',
                  'responsibilityTypes', 'institutionTypes', 'databaseLicenseNames', 
                  'apiTypes', 'pidSystems', 'qualityManagement', 'aidSystems',
                  'certificates', 'syndicationTypes', 'databaseLicenseURL', 
                  'dataUploadLicenseURL', 'name',)


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ('name',)


class RepositorySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    alt_names = serializers.StringRelatedField(many=True)

    class Meta:
        model = Repository
        fields = ('name', 'alt_names', 'url', 'persistent_url', 'accepted_taxonomy', 
                  'standards', 'owner', 'accepted_content', 'description', 'hosting_institution',
                  'institution_country', 'contact', 'size', 'date_operational', 
                  'metadataStandardName', 'metadataStandardURL', 'metadataRemarks',)
