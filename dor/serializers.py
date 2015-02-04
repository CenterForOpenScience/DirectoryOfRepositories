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
    accessTypes = serializers.MultipleChoiceField(choices=[('open', 'open'), ('embargoed', 'embargoed'), ('restricted', 'restricted'), ('closed', 'closed')])
    providerTypes = serializers.MultipleChoiceField(choices=[('dataProvider', 'dataProvider'), ('serviceProvider', 'serviceProvider')])
    responsibilityTypes = serializers.MultipleChoiceField(choices=[('funding', 'funding'), ('general', 'general'), ('sponsoring', 'sponsoring'), ('technical', 'technical')])
    apiTypes = serializers.MultipleChoiceField(choices=[('API', 'API'), ('FTP', 'FTP'), ('OAI-PMH', 'OAI-PMH'), ('REST', 'REST'), ('SOAP', 'SOAP'), ('SPARQL', 'SPARQL'), ('SWORD', 'SWORD'), ('other', 'other')])
    pidSystems = serializers.MultipleChoiceField(choices=[('ARK', 'ARK'), ('DOI', 'DOI'), ('HDL', 'HDL'), ('PURL', 'PURL'), ('URN', 'URN'), ('other', 'other'), ('none', 'none')])
    aidSystems = serializers.MultipleChoiceField(choices=[('AuthorClaim', 'AuthorClaim'), ('ISNI ORCID', 'ISNI ORCID'), ('ResearchedID', 'ResearchedID'), ('other', 'other'), ('none', 'none')])
    certificates = serializers.MultipleChoiceField(choices=[('CLARIN Certificate B', 'CLARIN Certificate B'), ('DIN 31644', 'DIN 31644'), ('DINI Certificate', 'DINI Certificate'), ('DRAMBORA', 'DRAMBORA'), ('DSA', 'DSA'), ('ISO 16363', 'ISO 16363'), ('ISO 16919', 'ISO 16919'), ('RatSWD', 'RatSWD'), ('TRAC', 'TRAC'), ('Trusted Digital Repository', 'Trusted Digital Repository'), ('WDS', 'WDS'), ('other', 'other')])
    syndicationTypes = serializers.MultipleChoiceField(choices=[('ATOM', 'ATOM'), ('RSS', 'RSS')])
    
    class Meta:
        model = Standards
        fields = ('databaseAccessTypes', 'accessTypes', 'dataUploadTypes',
                  'repositoryTypes', 'providerTypes', 'enhancedPublications',
                  'responsibilityTypes', 'institutionTypes', 'databaseLicenseNames',
                  'apiTypes', 'pidSystems', 'qualityManagement', 'aidSystems',
                  'certificates', 'syndicationTypes', 'databaseLicenseURL',
                  'dataUploadLicenseURL', 'name', 'owner',)


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        fields = ('name',)


class RepositorySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Repository
        fields = ('name', 'alt_names', 'url', 'persistent_url', 'accepted_taxonomy',
                  'standards', 'owner', 'accepted_content', 'description', 'hosting_institution',
                  'institution_country', 'contact', 'size', 'date_operational',
                  'metadataStandardName', 'metadataStandardURL', 'metadataRemarks')
