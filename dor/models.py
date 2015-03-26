from django.db import models
import datetime
from treebeard.ns_tree import NS_Node


class Journal(models.Model):
    name = models.CharField(max_length=100, default='')
    owner = models.ForeignKey('auth.User', related_name='journals')
    url = models.URLField()
    repos_endorsed = models.ManyToManyField('Repository',)
    # add embargo_period

    def __str__(self):
        return str(self.name)


class Taxonomy(NS_Node):
    name = models.CharField(max_length=100, default='')
    tax_id = models.IntegerField(null=True, blank=True)
    associated_content = models.ManyToManyField('ContentType',)

    node_order_by = ['tax_id', 'name']

    def __str__(self):
        if not self.is_root():
            return '{} - {}'.format(self.get_parent().__str__(), self.name)
        else:
            return '{}'.format(self.name)


class Standards(models.Model):
    name = models.CharField(max_length=100, default='')
    owner = models.ForeignKey('auth.User', related_name='standards')

    databaseAccessTypes = models.CharField(max_length=100, default='', choices=[('open','open'), ('restricted', 'restricted'), ('closed','closed'),])
    accessTypes = models.CharField(max_length=100, default='', choices=[('open','open'), ('embargoed', 'embargoed'), ('restricted', 'restricted'), ('closed', 'closed')])
    dataUploadTypes = models.CharField(max_length=100, default='', choices=[('open','open'), ('restricted', 'restricted'), ('closed', 'closed'),])
    repositoryTypes = models.CharField(max_length=100, default='', choices=[('disciplinary','disciplinary'), ('institutional', 'institutional'), ('other', 'other'),])
    providerTypes = models.CharField(max_length=100, default='', choices=[('dataProvider', 'dataProvider'), ('serviceProvider', 'serviceProvider')])
    responsibilityTypes = models.CharField(max_length=100, default='', choices=[('funding','funding'), ('general','general'), ('sponsoring', 'sponsoring'), ('technical', 'technical')])
    institutionTypes = models.CharField(max_length=100, default='', choices=[('commercial','commercial'), ('non-profit', 'non-profit')])
    databaseLicenseNames = models.CharField(max_length=100, default='', choices=[('Apache License 2.0', 'Apache License 2.0'), ('BSD', 'BSD'), ('CC', 'CC'), ('CC0', 'CC0'), ('Copyrights', 'Copyrights'), ('ODC', 'ODC'), ('Public Domain', 'Public Domain'), ('other', 'other')])
    databaseLicenseURL = models.URLField(default='')
    dataUploadLicenseURL = models.URLField(default='')
    apiTypes = models.CharField(max_length=100, default='', choices=[('API', 'API'), ('FTP', 'FTP'), ('OAI-PMH', 'OAI-PMH'), ('REST', 'REST'), ('SOAP', 'SOAP'), ('SPARQL', 'SPARQL'), ('SWORD', 'SWORD'), ('other', 'other')])
    pidSystems = models.CharField(max_length=100, default='', choices=[('ARK', 'ARK'), ('DOI', 'DOI'), ('HDL', 'HDL'), ('PURL', 'PURL'), ('URN', 'URN'), ('other', 'other'), ('none', 'none')])
    aidSystems = models.CharField(max_length=100, default='', choices=[('AuthorClaim', 'AuthorClaim'), ('ISNI ORCID', 'ISNI ORCID'), ('ResearchedID', 'ResearchedID'), ('other', 'other'), ('none', 'none')])
    enhancedPublications = models.CharField(max_length=100, default='', choices=[('yes', 'yes'), ('no', 'no'), ('unknown', 'unknown')])
    qualityManagement = models.CharField(max_length=100, default='', choices=[('yes', 'yes'), ('no', 'no'), ('unknown', 'unknown')])
    certificates = models.CharField(max_length=100, default='', choices=[('CLARIN Certificate B', 'CLARIN Certificate B'), ('DIN 31644', 'DIN 31644'), ('DINI Certificate', 'DINI Certificate'), ('DRAMBORA', 'DRAMBORA'), ('DSA', 'DSA'), ('ISO 16363', 'ISO 16363'), ('ISO 16919', 'ISO 16919'), ('RatSWD', 'RatSWD'), ('TRAC', 'TRAC'), ('Trusted Digital Repository', 'Trusted Digital Repository'), ('WDS', 'WDS'), ('other', 'other')])
    syndicationTypes = models.CharField(max_length=100, default='', choices=[('ATOM', 'ATOM'), ('RSS', 'RSS')])

    node_order_by = ['name']

    def __str__(self):
        return '{0} Standards'.format(self.name)


class ContentType(NS_Node):
    name = models.CharField(max_length=100, default='')

    node_order_by = ['name']

    def __str__(self):
        return '{0}'.format(self.name)


class Repository(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    alt_names = models.CharField(max_length=200, blank=True, default='')
    url = models.URLField()
    persistent_url = models.URLField(null=True, default='')
    accepted_taxonomy = models.ManyToManyField('Taxonomy',)
    accepted_content = models.ManyToManyField('ContentType',)
    standards = models.ForeignKey('Standards', related_name='standards')
    description = models.CharField(max_length=1000, blank=True, default='')
    hosting_institution = models.CharField(max_length=100, blank=True, default='')
    institution_country = models.CharField(max_length=100, blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='repositorys')
    contact = models.CharField(max_length=100, blank=True, default='')
    metadataStandardName = models.CharField(max_length=200, default='')
    metadataStandardURL = models.URLField()
    metadataRemarks = models.CharField(max_length=1000, blank=True, default='')
    size = models.IntegerField(default=0)
    date_operational = models.DateField(default=datetime.date(1900, 1, 1))
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ('date_operational',)

    def __str__(self):
        return str(self.name)
