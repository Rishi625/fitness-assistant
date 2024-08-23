from .web_search_api import BingSearch
from assets.fitness_websites import 

bing_search = BingSearch()


def search_web(queries):
    results = []

    for query in queries:
        results.append({'query' : query, 'results' : bing_search.search()})

    return results


def filter_results(results):


