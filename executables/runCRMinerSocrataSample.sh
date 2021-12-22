#Socrata:
filepath="data/socrata/column_table_changes_aggregated_grouped.json"
timepointsFile="data/timepointsSocrata.json"
#10 Threads:
echo "Processing Socrata"
samplingRates=("0.001" "0.005" "0.01" "0.05" "0.1" "0.2" "0.3" "0.4" "0.5")
nThreadsList=("1")
mkdir logsSampling/
mkdir logsSampling/socrata/
mkdir runtimeLogs/
mkdir runtimeLogs/socrata/

for nThreads in "${nThreadsList[@]}"
do
      for samplingRate in "${samplingRates[@]}"
      do
         echo "Processing nthreads $nThreads with samplingRate $samplingRate"
         outputFilePath="data/socrata/crminer_nthreads${nThreads}_${samplingRate}.txt"
         logPath="logsSampling/socrata/crminer_nthreads${nThreads}_${samplingRate}.txt"
         # or do whatever with individual element of the array
         start_time=$(date +%s)
         code/mining-change-rules/rule_generation/create_histograms.py $filepath $timepointsFile $outputFilePath --min_sup 0.05 --max_sup 0.45 --min_conf 0.9 --num_bins 11 -s 200 --threads $nThreads --sample_size $samplingRate > $logPath 2>&1
         end_time=$(date +%s)
         elapsed=$(( end_time - start_time ))
         echo "Took $elapsed seconds" > "runtimeLogs/socrata/crminer_nthreads${nThreads}_${samplingRate}.txt"
      done
done
