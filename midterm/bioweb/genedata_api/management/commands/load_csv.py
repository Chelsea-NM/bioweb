from django.core.management.base import BaseCommand
from genedata_api.models import proteins, domains, domainAssignment
import csv


class Command(BaseCommand):
    help = 'Load data from CSV files into the models'

    def add_arguments(self, parser):
        parser.add_argument('csv_files', nargs='+', type=str,
                            help='Paths to the CSV files')

    def handle(self, *args, **options):
        csv_files = options['csv_files']

        # Clear existing data in all models
        proteins.objects.all().delete()
        domains.objects.all().delete()
        domainAssignment.objects.all().delete()

        # Load data from CSV files into models
        for csv_file in csv_files:
            with open(csv_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row if present

                if csv_file.endswith('assignment_data_sequences.csv'):
                    self.load_proteins(reader)
                elif csv_file.endswith('pfam_descriptions.csv'):
                    self.load_domains(reader)
                elif csv_file.endswith('assignment_data_set.csv'):
                    self.load_domain_assignment(reader)

    def load_proteins(self, reader):
        for row in reader:
            protein = proteins(
                proteinID=row[0],
                sequence=row[1],
            )
            protein.save()

    def load_domains(self, reader):
        for row in reader:
            domain = domains(
                domainID=row[0],
                pfamFamilyDescription=row[1],
            )
            domain.save()

    def load_domain_assignment(self, reader):
        for row in reader:
            domain_assignment = domainAssignment(
                protein_id=row[0],
                organismTaxaID=row[1],
                organismCladeIdenitifer=row[2],
                organismScientificName=row[3],
                domainDescription=row[4],
                domainID_id=row[5],
                domainStart=row[6],
                domainEndCoordinate=row[7],
                lengthProtein=row[8],
            )
            domain_assignment.save()
