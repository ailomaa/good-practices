#!/bin/bash
#
# Run the word frequency count on the sample data.
# Expects an activated virtual environment - see README.md.

mkdir -p results

python3 wordfreq.py data/sample.txt \
    --top 15 \
    --min-length 4 \
    --ascii \
    --output results/top-words.txt

echo "Done. Results in results/top-words.txt"
