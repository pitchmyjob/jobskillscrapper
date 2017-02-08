from django.core.management.base import BaseCommand


from ._scrapper import ScrapperHandler


class Command(BaseCommand):
    help = 'Parse an profile to retrieve jobs & skills'

    def add_arguments(self, parser):
        parser.add_argument('--service', type=str)
        parser.add_argument('link', type=str)

    def handle(self, *args, **options):
        self.stdout.write('# Starting scrapper')

        service = options.get('service')
        links = [options.get('link')]

        ScrapperHandler(service=service, urls=links)

        self.stdout.write('\n# Ending scrapper')
