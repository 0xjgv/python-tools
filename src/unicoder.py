from dig import get_mx_servers, get_all_mxs
from collections import defaultdict
from unidecode import unidecode
from json import loads, dump
from asyncio import run
from sys import argv


def build_translations():
    translator = defaultdict(set)
    for i in range(5000, 9000):
        char = chr(i).lower()
        if char:
            base = unidecode(char).lower()
            if base != char and base.isalpha() and len(base) == 1:
                translator[base].add(char)
    return {k: list(v) for k, v in translator.items()}


def get_domain_combinations():
    if len(argv) < 2:
        print("Pass a domain sample.")
        return

    domain = argv[1]

    translations_path = f"translations/{domain}.json"
    domain, *tlds = domain.rsplit('.')

    try:
        with open(translations_path, "r") as file:
            translations = loads(file)
    except:
        translations = build_translations()
        with open(translations_path, "w") as file:
            dump(translations, file)

    tld = ".".join(tlds)
    combinations = set()
    for i, c in enumerate(domain):
        dom = [d for d in domain]
        for pos in sorted(translations.get(c, set())):
            dom[i] = pos
            combinations.add(f"{''.join(dom)}.{tld}")
    return combinations


if __name__ == "__main__":
    domain_combinations = get_domain_combinations()
    mxs = run(get_all_mxs(domain_combinations))
    print(mxs)
