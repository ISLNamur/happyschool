from django.core.management.base import BaseCommand

from core.models import TeachingModel
from core.adminsettings.importclass import ImportStudentLDAP, ImportResponsibleLDAP


class Command(BaseCommand):
    help = 'Sync django database from a LDAP server.'

    def add_arguments(self, parser):
        parser.add_argument(
            "-p",
            '--people',
            help='Sync only some people (responsible or student)'
        )

    def handle(self, *args, **options):
        teachings = TeachingModel.objects.all()
        if not options['people'] or options['people'] == "student":
            for t in teachings:
                importation = ImportStudentLDAP(t)
                importation.sync()

        if not options['people'] or options['people'] == "responsible":
            for t in teachings:
                importation = ImportResponsibleLDAP(t)
                importation.sync()
