import json
import sys
import time
import datetime
import timeit

from episode_mining.minepi import MINEPI, MinEpiRules
from episode_mining.winepi import WINEPI, WinEpiRules

def reportFileStatistics(timestampToEventDict,eventsSorted):
    print("Num Timestamps,",len(timestampToEventDict))
    print("Alphabet Size",len(eventsSorted))
    size = sum(list(map(lambda kv: len(kv[1]), timestampToEventDict.items())))
    print("Total Num Events",size)
    print("AVG Events per Timestamp",size / len(timestampToEventDict))
    print("AVG Frequency per Event Type", size / len(eventsSorted) )

def parseDateTime(x):
    if ('T' not in x):
        x = x + 'T0'
    return datetime.datetime.strptime(x, "%Y-%m-%dT%H")

def loadTimestampToEventDictFromFile():
    file = open(dataFile)
    res = json.load(file)
    file.close()
    timestampToEventDict = {}
    keysSorted = sorted(res.keys())
    for i,key in enumerate(keysSorted):
        timestamps = sorted(list(map(lambda x: parseDateTime(x), res[key])))
        for ts in timestamps:
            eventList = timestampToEventDict.get(ts)
            if eventList is not None:
                eventList.append(i)
            else:
                newList = [i]
                timestampToEventDict[ts] = newList
    return timestampToEventDict,keysSorted

def main():
    print("Starting Data Loading")
    # print(timestampToEventDict)
    timestampToEventDict,eventsSorted = loadTimestampToEventDictFromFile()
    reportFileStatistics(timestampToEventDict,eventsSorted)

if __name__ == "__main__":
    print('Number of arguments:', len(sys.argv), 'arguments.')
    sys.stdout.flush()
    print('Argument List:', str(sys.argv))
    sys.stdout.flush()
    dataFile = sys.argv[1]
    main()
