import datetime
from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    user_type = models.CharField(max_length=100, default='', choices=[('Repository Representative', 'Repository Representative'), ('Journal Representative', 'Journal Representative')])
    maintains_obj = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)


class Journal(models.Model):
    name = models.CharField(max_length=100, default='')
    owner = models.ForeignKey('auth.User', related_name='journals')
    url = models.URLField()
    repos_endorsed = models.ManyToManyField('Repository', blank=True)

    is_visible = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


class Taxonomy(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    obj_name = models.CharField(max_length=100, default='')
    tax_id = models.IntegerField(null=True, blank=True)
    associated_content = models.ManyToManyField('ContentType', blank=True)
    embargoed = models.BooleanField(default=True, verbose_name='Hidden on site')

    def __str__(self):
        return '{}'.format(self.obj_name)

    class Meta:
        verbose_name_plural = 'Taxonomies'

    class MPTTMeta:
        order_insertion_by = ['obj_name']


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

    class Meta:
        verbose_name_plural = 'Standards'


class Certification(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    obj_name = models.CharField(max_length=100, default='')

    node_order_by = ['obj_name']

    def __str__(self):
        return '{0}'.format(self.obj_name)


class ContentType(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    obj_name = models.CharField(max_length=100, default='')
    associated_repo = models.ForeignKey('Repository', related_name='specific_data_types', blank=True, null=True)
    token_id = models.CharField(max_length=32, blank=True, null=True, default='')

    node_order_by = ['obj_name']

    def __str__(self):
        return '{0}'.format(self.obj_name)


class Repository(models.Model):
    name = models.CharField(max_length=100, default='')
    alt_names = models.CharField(max_length=200, blank=True, default='')
    url = models.URLField(verbose_name="Repository URL")
    persistent_url = models.URLField(null=True, blank=True, default='')
    accepted_taxonomy = TreeManyToManyField('Taxonomy',)
    accepted_content = TreeManyToManyField('ContentType',)
    #standards = models.ForeignKey('Standards', related_name='standards', null=True)
    description = models.CharField(max_length=1000, blank=True, default='')
    hosting_institution = models.CharField(max_length=100, blank=True, default='')
    institution_country = models.CharField(max_length=100, blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='repositorys', null=True, blank=True)
    contact = models.CharField(max_length=100, blank=True, default='')
    metadataInformationURL = models.URLField(verbose_name="Metadata Information URL")
    metadataRemarks = models.CharField(max_length=1000, blank=True, default='', verbose_name="Metadata Remarks")
    size = models.IntegerField(default=0)
    date_operational = models.DateField(default=datetime.date.today())
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    remarks = models.CharField(max_length=10000, default='')
    embargoed = models.BooleanField(default=True, verbose_name='Hidden on site')
    allows_embargo_period = models.BooleanField(default=False)
    doi_provided = models.BooleanField(default=False)
    links_to_publications = models.BooleanField(default=False)
    db_certifications = TreeManyToManyField('Certification', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Repositories'

    def __str__(self):
        return str(self.name)
