timepointsFile="data/timepointsWikipedia.json"
outputRootPath="data/results/wikipedia/"

#!/bin/bash
for filepath in data/wikipedia/*.json; do
	echo "Processing $filepath"
	filename=$(basename $filepath)
	outputFilePath="$outputRootPath/$filename"
	code/discovering-change-dependencies/rule_generation/create_histograms.py $filepath $timepointsFile $outputFilePath --min_sup 0.0005475701574264203 --max_sup 0.45 --min_conf 0.9 --num_bins 24 -s 10000
done
