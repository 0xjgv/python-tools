#!/usr/bin/env python3
from argparse import Namespace, ArgumentParser
from collections import Counter, defaultdict
from typing import List
from re import sub
import argparse
import math
import sys


def entropy_lines(lines: List[str]) -> float:
    results = []
    for line in lines:
        chrs = sub(r"[^\w]", "", line.lower().strip())
        counts = Counter(chrs)
        length = len(chrs)
        prob = [float(c) / length for c in counts.values()]
        entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob])
        results.append((entropy, line))
    return results


def parse_options(args: List[str]) -> Namespace:
    parser = ArgumentParser(
        prog="entropy", description=("Measure the entropy of a string"),
    )
    parser.add_argument("text", nargs="+", help="Text you want to calculate entropy")
    parser.add_argument(
        "-n", "--number", default=10, help="Display n largest entropy values"
    )
    return parser.parse_args(args)


def run(args: Namespace) -> None:
    n = abs(int(args.number))
    results = entropy_lines(args.text)
    for score, line in sorted(results)[-n:]:
        print(f"--- Line ---\n{line}")
        print(f"Entropy: {score}")


if __name__ == "__main__":
    if sys.stdin.isatty():
        run(parse_options(sys.argv[1:]))
    else:
        lines = [l.strip() for l in sys.stdin]
        run(parse_options(sys.argv[1:] + lines))
