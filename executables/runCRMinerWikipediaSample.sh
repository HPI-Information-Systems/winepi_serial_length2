#wikipedia:
timepointsFile="data/timepointsWikipedia.json"
outputRootPath="data/results/wikipedia/"
#10 Threads:
echo "Processing wikipedia"
samplingRates=("0.000001" "0.000005" "0.00001" "0.00002" "0.00005" "0.0001" "0.001" "0.005" "0.01" "0.05" "0.1" "0.2" "0.3" "0.4" "0.5")

nThreadsList=("10" "1")
mkdir logsSampling/
mkdir logsSampling/wikipedia/
mkdir runtimeLogs/
mkdir runtimeLogs/wikipedia/

for nThreads in "${nThreadsList[@]}"
do
      for samplingRate in "${samplingRates[@]}"
      do
         echo "Processing nthreads $nThreads with samplingRate $samplingRate"
         outputFilePath="data/results/wikipedia/crminer_nthreads${nThreads}_${samplingRate}.txt"
         # or do whatever with individual element of the array
         start_time=$(date +%s)
         for filepath in data/wikipedia/*.json; do
            fname="$(basename -- $filepath)"
            logPath="logsSampling/wikipedia/crminer_${fname}_nthreads${nThreads}_${samplingRate}.txt"
            echo "Processing $filepath"
            filename=$(basename $filepath)
            outputFilePath="$outputRootPath/$filename"
            code/mining-change-rules/rule_generation/create_histograms.py $filepath $timepointsFile $outputFilePath --min_sup 0.0005475701574264203 --max_sup 0.45 --min_conf 0.9 --num_bins 24 -s 10000
         done

         #code/mining-change-rules/rule_generation/create_histograms.py $filepath $timepointsFile $outputFilePath --min_sup 0.05 --max_sup 0.45 --min_conf 0.9 --num_bins 11 -s 200 --threads $nThreads --sample_size $samplingRate > $logPath 2>&1
         end_time=$(date +%s)
         elapsed=$(( end_time - start_time ))
         echo "Took $elapsed seconds" > "runtimeLogs/wikipedia/crminer_nthreads${nThreads}_${samplingRate}.txt"
      done
done
