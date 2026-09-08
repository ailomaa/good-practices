#!/usr/bin/env python3
"""Count the most common words in a text file.

Deliberately depends on two packages from requirements.txt, so it will not
run outside an activated virtual environment.
"""

import argparse
import re
import sys
from collections import Counter

from tabulate import tabulate
from unidecode import unidecode

# A word is a run of letters, optionally joined by an apostrophe or a hyphen:
# "don't" and "code-switching" are one word each. Digits and underscores are
# not letters, so "session_3" yields "session" and "2026" is ignored.
WORD = re.compile(r"[^\W\d_]+(?:['’-][^\W\d_]+)*", re.UNICODE)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Count the most common words in a text file."
    )
    parser.add_argument(
        "input",
        help="text file to read",
    )
    parser.add_argument(
        "--top",
        type=int,
        required=True,
        metavar="N",
        help="how many words to report (required)",
    )
    parser.add_argument(
        "--min-length",
        type=int,
        default=1,
        metavar="N",
        help="ignore words shorter than this (default: 1)",
    )
    parser.add_argument(
        "--ascii",
        action="store_true",
        help="fold accented characters to ASCII, so that 'än' and 'an' count together",
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        help="write the table here instead of to the screen",
    )
    return parser.parse_args()


def count_words(text, min_length, to_ascii):
    if to_ascii:
        text = unidecode(text)
    words = (w.lower() for w in WORD.findall(text))
    return Counter(w for w in words if len(w) >= min_length)


def main():
    args = parse_args()

    try:
        with open(args.input, encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        sys.exit(f"error: no such file: {args.input}")

    counts = count_words(text, args.min_length, args.ascii)
    if not counts:
        sys.exit("error: no words matched - is --min-length too high?")

    total = sum(counts.values())
    rows = [
        (rank, word, n, f"{100 * n / total:.1f}%")
        for rank, (word, n) in enumerate(counts.most_common(args.top), start=1)
    ]
    table = tabulate(rows, headers=["#", "word", "count", "share"])

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(table + "\n")
        print(f"wrote {args.output} ({len(counts)} distinct words, {total} total)")
    else:
        print(table)


if __name__ == "__main__":
    main()
