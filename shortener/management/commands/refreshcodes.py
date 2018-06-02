from django.core.management.base import BaseCommand, CommandError

from shortener.models import thwURL


class Command(BaseCommand):
	help = 'Refrehes all thwURL shortcodes'
	def add_arguments(self, parser):
		parser.add_argument('--items', type=int)
		
	def handle(self, *args, **options):
		return thwURL.objects.refresh_shortcodes(items=options['items'])
