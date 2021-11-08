from argparse import Namespace, ArgumentParser
from collections import Counter
from functools import lru_cache
from typing import List, Tuple
from re import split
import math
import sys


@lru_cache(maxsize=None)
def calculate_entropy(s):
    p, lns = Counter(s), float(len(s))
    return -sum(count / lns * math.log(count / lns, 2) for count in p.values())


def entropy_lines(lines: List[str]) -> List[Tuple[float, str]]:
    all_lines = list(filter(bool, map(str.strip, lines)))
    results = []
    for line in all_lines:
        for w in split(r" |_", line.lower()):
            entropy = calculate_entropy(w)
            if entropy > 0:
                results.append((round(entropy, 3), line))
    return results


def parse_options(args: List[str]) -> Namespace:
    parser = ArgumentParser(
        prog="entropy",
        description=("Measure the entropy of a string"),
    )
    parser.add_argument("text", nargs="+", help="Text you want to calculate entropy")
    parser.add_argument(
        "-n", "--number", default=5, help="Display n largest entropy values. Default: 5"
    )
    return parser.parse_args(args)


def run(args: Namespace) -> None:
    n = abs(int(args.number))
    results = entropy_lines(args.text)
    for score, line in sorted(results)[-n:]:
        print(score, line)
        print(f"--- Line ---\n{line[:50]}...")
        print(f"Entropy: {score}")
        print(f"Length: {len(line)}")


def main():
    if sys.stdin.isatty():
        run(parse_options(sys.argv[1:]))
    else:
        lines = list(map(str.strip, sys.stdin))
        run(parse_options(sys.argv[1:] + lines))


if __name__ == "__main__":
    main()
