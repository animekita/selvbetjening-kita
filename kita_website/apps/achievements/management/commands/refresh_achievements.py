from django.core.management.base import BaseCommand, CommandError

from kita_website.apps.achievements.models import refresh_achievements_handlers

class Command(BaseCommand):
    def handle(self, *args, **options):

        for handler in refresh_achievements_handlers:
            handler()