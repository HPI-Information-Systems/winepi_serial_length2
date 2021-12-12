timepointsFile="../../data/timepointsSocrata.json"
outputRootPath="../../data/results/socrata/"

python3 Main.py "MINEPI" "../../data/socrata/column_table_changes_aggregated_grouped.json" > ../../logs/minepiLog.txt 2>&1

