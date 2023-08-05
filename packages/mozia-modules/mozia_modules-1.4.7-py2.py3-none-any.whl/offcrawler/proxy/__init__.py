from .farfetch import crawl_farfetch_product
from .intramirror import crawl_intramirror_product


def crawl_product(catalog):
    if 1 == catalog["source_type"]:
        return crawl_farfetch_product(catalog)
    elif 3 == catalog["source_type"]:
        return crawl_intramirror_product(catalog)
