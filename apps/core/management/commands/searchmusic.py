from email.policy import default

from django.core.management.base import BaseCommand
from apps.carolerApi.caroler import CarolerApi
class Command(BaseCommand):
    help = "➡ this is help of search music command"

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help="count page")

    def handle(self, *args, **kwargs):
        count = kwargs.get('count',None)
        CarolerApi.new_music(cont_page=count)