from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Describe the Command Here"
    def handle_noargs(self, **options):
