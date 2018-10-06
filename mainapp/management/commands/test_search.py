import time
from typing import Dict, List

from django.core.management import call_command
from django.core.management.base import BaseCommand

from mainapp.documents.index import elastic_index
from mainapp.functions.search_tools import search_string_to_params, MainappSearch, parse_hit


class Command(BaseCommand):
    help = 'Search for some predefined terms to check how the search is working'

    def add_arguments(self, parser):
        parser.add_argument('--rebuild', action="store_true")

    def analyze(self, text: str) -> Dict[str, List[Dict]]:
        """ Shows what elasticsearch does with the tokens """
        return elastic_index.analyze(
            analyzer="text_analyzer",
            text=text
        )

    def handle(self, *args, **options):
        """
        The checks:
         * "rese" should match "research", but currently doesn't
         * "contain(|sng|ing)" should match "containing" by stemming, preserving the original and fuzzy
         * "here" matches "here's" due to language analysis
         * "Knutt" should prefer "Knutt" over "Knuth", but currently prefers ferequency
         * "Schulhaus" is for big german dataset performance
        """
        if options.get("rebuild"):
            start = time.perf_counter()
            call_command('search_index', action='rebuild', force=True, models=["mainapp.Person"])
            end = time.perf_counter()
            print(f"Total: {end - start}")

        words = ["containing", "here's"]

        for word in words:
            print(word, [token['token'] for token in self.analyze(word)["tokens"]])

        queries = ["rese", "contain", "containsng", "containing", "here", "Knutt", "Schulhaus"]
        for query in queries:
            params = search_string_to_params(query)
            main_search = MainappSearch(params)
            executed = main_search.execute()
            print(f"# {query}: {len(executed.hits)} | {executed.took}")
            for hit in executed.hits:
                hit = parse_hit(hit)
                highlight = str(hit.get('highlight')).replace("\n", " ").replace("\r", " ")[:100]
                print(f" - {hit['name'][:30]} | {highlight}")
