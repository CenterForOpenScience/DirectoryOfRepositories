from rest_framework import serializers
from rest_framework.reverse import reverse
from dor.models import Repository, Taxonomy, Standards,\
    ContentType, Journal
from django.contrib.auth.models import User
from collections import OrderedDict


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username',)


class JournalSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Journal
        fields = ('name', 'repos_endorsed', 'owner', 'remarks')


class TaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxonomy
        fields = ('name', 'tax_id', 'associated_content')


class StandardsSerializer(serializers.ModelSerializer):
    accessTypes = serializers.MultipleChoiceField(choices=[('open', 'open'), ('embargoed', 'embargoed'), ('restricted', 'restricted'), ('closed', 'closed')])
    providerTypes = serializers.MultipleChoiceField(choices=[('dataProvider', 'dataProvider'), ('serviceProvider', 'serviceProvider')])
    responsibilityTypes = serializers.MultipleChoiceField(choices=[('funding', 'funding'), ('general', 'general'), ('sponsoring', 'sponsoring'), ('technical', 'technical')])
    apiTypes = serializers.MultipleChoiceField(choices=[('API', 'API'), ('FTP', 'FTP'), ('OAI-PMH', 'OAI-PMH'), ('REST', 'REST'), ('SOAP', 'SOAP'), ('SPARQL', 'SPARQL'), ('SWORD', 'SWORD'), ('other', 'other')])
    pidSystems = serializers.MultipleChoiceField(choices=[('ARK', 'ARK'), ('DOI', 'DOI'), ('HDL', 'HDL'), ('PURL', 'PURL'), ('URN', 'URN'), ('other', 'other'), ('none', 'none')])
    aidSystems = serializers.MultipleChoiceField(choices=[('AuthorClaim', 'AuthorClaim'), ('ISNI ORCID', 'ISNI ORCID'), ('ResearchedID', 'ResearchedID'), ('other', 'other'), ('none', 'none')])
    certificates = serializers.MultipleChoiceField(choices=[('CLARIN Certificate B', 'CLARIN Certificate B'), ('DIN 31644', 'DIN 31644'), ('DINI Certificate', 'DINI Certificate'), ('DRAMBORA', 'DRAMBORA'), ('DSA', 'DSA'), ('ISO 16363', 'ISO 16363'), ('ISO 16919', 'ISO 16919'), ('RatSWD', 'RatSWD'), ('TRAC', 'TRAC'), ('Trusted Digital Repository', 'Trusted Digital Repository'), ('WDS', 'WDS'), ('other', 'other')])
    syndicationTypes = serializers.MultipleChoiceField(choices=[('ATOM', 'ATOM'), ('RSS', 'RSS')])

    def to_representation(self, instance):
        if self.context['request'].method == 'POST':
            return super(StandardsSerializer, self).to_representation(instance)
        else:
            ret = OrderedDict()
            fields = [field for field in self.fields.values() if not field.write_only]
            for field in fields:
                # TODO: Find another better way of doing this
                if field.field_name == 'owner':
                    user = User.objects.get(id=field.to_representation(field.get_attribute(instance)))
                    ret[field.field_name] = 'http://localhost:8000' + reverse('user-detail', [user.id])
                else:
                    ret[field.field_name] = field.get_attribute(instance)
                    if ret[field.field_name][0] == '{':
                        ret[field.field_name] = eval(ret[field.field_name])
            return ret

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
                  'metadataInformationURL', 'metadataRemarks', 'remarks',
                  'allows_embargo_period', 'doi_provided', 'links_to_publications')
