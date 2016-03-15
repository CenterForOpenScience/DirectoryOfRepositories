import datetime
import sys

import xlrd

from django.core.management.base import BaseCommand
from dor.models import Repository, User

if sys.version[0] == '3':
    unicode = str

class Command(BaseCommand):
    help = 'Imports Repository data from a spreadsheet'
    """ Cleaned - RE3 Earth Science repositories (1).xlsx
        ##########################################
        Column names:           - model attr names
        ------------------------------------------
    1   RepositoryName          - name
    2   RepositoryURL           - url
    3   Description             - description
    4   Repository Contact      - contact
    5   Size                    - size
    6   Start Date              - date_operational
    7   MissionStatementURL     - metadataInformationUrl
    8   Inst. Contact           - contact (if not contact), else remarks
    9   Remarks                 - remarks
    10  Provider type           - N/A, append to remarks
    11  Keywords                - accepted_taxonomy / accepted_content / remarks
    12  Inst. Name              - hosting_institution
    13  DatabaseAccessType      - N/A, append to remarks
    14  PIDSystem               - doi_provided (True iff truthy), append to remarks
    15  enhnace pubs            - N/A, append to remarks
    16  quality mgmt            - N/A, append to remarks
    17  datauploadtype          - N/A, append to remarks

        ##############################################
        Required attributes:    (frequency of absence)
        ----------------------------------------------
        name                    (rarely/never)
        url                     (rarely/never)
        accepted_taxonomy       (never absent, always unparseable)
        accepted_content        (never absent, always unparseable)
        metadataInformationUrl  (frequently)
        size                    (frequently)
        date_operational        (frequently)
        remarks                 (probably never)
    """
    def add_arguments(self, parser):
        parser.add_argument('fp', nargs='+', type=str)

    def handle(self, *args, **options):
        owner = User.objects.filter(is_superuser=True)[0]
        migrated_repos = []

        wb = xlrd.open_workbook(options['fp'][0])
        sheet = wb.sheets()[0]
        for row in (sheet.row(index) for index in range(1, sheet.nrows)):
            name = self.strip_unicode(row, 1)
            url = self.strip_unicode(row, 2)
            description = self.strip_unicode(row, 3)
            contact = self.strip_unicode(row, 4)
            size = self.strip_unicode(row, 5) or 0
            date = self.parse_date(row[6], wb.datemode)
            metadata_url = self.strip_unicode(row, 7) or 'http://DEFAULT_VALUE.com'
            remarks = self.strip_unicode(row, 9)

            if not contact:
                contact = self.strip_unicode(row, 8)
            else:
                remarks = '{}\n\nInstitutional Contacts: {}'.format(
                    remarks, self.strip_unicode(row, 8))

            if remarks:
                remarks = '{}\n\nProvider Type: {}'.format(remarks,
                    self.strip_unicode(row, 10))
            else:
                remarks = 'Provider Type: {}'.format(self.strip_unicode(row, 10))

            remarks = '{}\n\nKeywords: {}'.format(remarks, self.strip_unicode(row, 11))
            hosting_institution = self.strip_unicode(row, 12)
            remarks = '{}\n\nDatabaseAccessType: {}'.format(remarks,
                self.strip_unicode(row, 13))
            doi_provided = self.strip_unicode(row, 14) not in ('', 'none')
            if doi_provided:
                remarks = '{}\n\nPIDSystem: {}'.format(
                    remarks, self.strip_unicode(row, 14))

            if row[15].value:
                remarks = '{}\n\nEnhances Publications: {}'.format(
                    remarks, self.strip_unicode(row, 15))
            if row[16].value:
                remarks = '{}\n\nQuality Management: {}'.format(
                    remarks, self.strip_unicode(row, 16))
            if row[17].value:
                remarks = '{}\n\nData Upload Type: {}'.format(
                    remarks, self.strip_unicode(row, 17))

            repo = Repository(
                owner=owner,
                name=name,
                url=url,
                description=description,
                contact=contact,
                size=size,
                date_operational=date,
                metadataInformationURL=metadata_url,
                remarks=remarks,
                hosting_institution=hosting_institution,
                doi_provided=doi_provided,
                embargoed=True
            )
            repo.save()

            migrated_repos.append(repo)
            print(u'Created {}'.format(name))
        print('Created {} new repositories'.format(len(migrated_repos)))

    def parse_date(self, cell, mode):
        if cell.ctype == 0:       # None
            return datetime.date(1900, 1, 1)
        elif cell.ctype == 1:     # String
            year = int(cell.value.split('-')[0])
            month = int(cell.value.split('-')[1])
            return datetime.date(year, month, 1)
        elif cell.ctype == 2:     # Float - number
            year = int(cell.value)
            return datetime.date(year, 1, 1)
        elif cell.ctype == 3:      # Float - xldate
            date_tuple = xlrd.xldate_as_tuple(cell.value, mode)[:3]
            return datetime.date(date_tuple[0], date_tuple[1], date_tuple[2])

    def strip_unicode(self, row, index):
        if type(row[index].value) is unicode:
            return ''.join([c for c in row[index].value if ord(c) < 128])
        else:
            return row[index].value
