from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db.utils import IntegrityError
from django.apps import apps
from glob import glob


class Command(BaseCommand):
    help = 'Fixture loader. Imports models from fixtures.'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('app_name',
                            nargs='*',
                            help='Provide at least one app name as is listed in INSTALLED_APPS',
                            type=str)

    def get_fixtures(self, app_name):
        fixtures = []
        for fixture_name in glob("{0}/fixtures/*.json".format(app_name)):
            fixtures.append({
                "name": fixture_name,
                "applied": False,
                "retries": 0,
            })
        return fixtures

    def get_app_names(self):
        return list(set([model._meta.app_label for model in apps.get_models()]))

    def handle(self, *args, **options):
        if ".production" in options["settings"]:
            fix = input("Fixtures will be imported in the PRODUCTION environment. Are you sure? [Y/n] ")
            if fix != "Y":
                self.stderr.write("Operation cancelled.")
                return False

        dump_app_names = options["app_name"] if options["app_name"] else self.get_app_names()

        for app_name in dump_app_names:
            fixtures = self.get_fixtures(app_name)
            while [fixture for fixture in fixtures if not fixture["applied"]]:
                for fixture in fixtures:
                    if fixture["applied"]:
                        continue
                    try:
                        self.stdout.write("Loading {0}...".format(fixture["name"]))
                        self.stdout.flush()
                        call_command("loaddata", fixture["name"])
                        fixture["applied"] = True
                        fixture["retries"] = 0
                    except IntegrityError as e:
                        self.stderr.write("[ FAILED ] Fixture " + fixture["name"] + ": " + e.args[0])
                        self.stdout.write("\tIt will be retried later...")
                        fixture["retries"] += 1
                if any(fixture["retries"] >= 5 for fixture in fixtures):
                    self.stderr.write("Couldn't load all fixtures.")
                    break
