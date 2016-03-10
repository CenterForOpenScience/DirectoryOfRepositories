import datetime

import xlrd

from django.core.management.base import BaseCommand
from dor.models import Repository, User

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
            name = row[1].value
            url = row[2].value
            description = row[3].value
            contact = row[4].value
            size = row[5].value or 0
            date = self.parse_date(row[6], wb.datemode)
            metadata_url = row[7].value or 'http://DEFAULT_VALUE.com'
            remarks = row[9].value

            if not contact:
                contact = row[8].value
            else:
                remarks = '{}\n\nIntitutional Contacts: {}'.format(remarks, row[8].value)

            if remarks:
                remarks = '{}\n\nProvider Type: {}'.format(remarks, row[10].value)
            else:
                remarks = 'Provider Type: {}'.format(row[10].value)

            remarks = '{}\n\nKeywords: {}'.format(remarks, row[11].value)
            hosting_institution = row[12].value
            remarks = '{}\n\nDatabaseAccessType: {}'.format(remarks, row[13].value)
            doi_provided = row[14].value not in ('', 'none')
            if doi_provided:
                remarks = '{}\n\nPIDSystem: {}'.format(remarks, row[14].value)

            if row[15].value:
                remarks = '{}\n\nEnhances Publications: {}'.format(remarks, row[15].value)
            if row[16].value:
                remarks = '{}\n\nQuality Management: {}'.format(remarks, row[16].value)
            if row[17].value:
                remarks = '{}\n\nData Upload Type: {}'.format(remarks, row[17].value)

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
            print('Created {}'.format(repo))
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
