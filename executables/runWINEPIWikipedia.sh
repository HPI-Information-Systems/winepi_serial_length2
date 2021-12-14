#!/bin/bash
for filepath in data/wikipedia/*.json; do
        echo "Processing $filepath"
        filename=$(basename $filepath)
        logPath="logsRelatedWork/${filename}.txt"
        python3 code/episodeMiningModified/Main.py "WINEPI" $filepath 24 1 0.0005475701574264203 0.9 1 > $logPath 2>&1
done