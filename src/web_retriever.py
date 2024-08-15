from .web_search_api import BingSearch


bing_search = BingSearch()


def search_web(queries):
    results = []

    for query in queries:
        results.append({'query' : query, 'results' : bing_search.search()})

    return results

