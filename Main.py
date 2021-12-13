import json
import sys
import time
import datetime
import timeit

from episode_mining.minepi import MINEPI, MinEpiRules
from episode_mining.winepi import WINEPI, WinEpiRules

def loadTimestampToEventDictFromFile(filePath):
    file = open(filePath)
    res = json.load(file)
    file.close()
    timestampToEventDict = {}
    keysSorted = sorted(res.keys())
    #keysSorted = keysSorted[-10:]
    for key in keysSorted:
        timestamps = sorted(list(map(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"),res[key])))
        for ts in timestamps:
            eventList = timestampToEventDict.get(ts)
            if eventList is not None:
                eventList.append(key)
            else:
                newList = [key]
                timestampToEventDict[ts] = newList
    return timestampToEventDict

def getTimestampToIntegerDict1DayIncrement(timestampsSorted):
    firstTimestamp = timestampsSorted[0]
    lastTimestamp = timestampsSorted[-1]
    #SOCRATA SPECIFIC: TODO - change this for Wikipedia!
    incrementInDays=1
    curTimestamp = firstTimestamp
    timestampToIntegerDict = {}
    curInteger = 0
    while curTimestamp != None:
        timestampToIntegerDict[curTimestamp] = curInteger
        curInteger+=1
        if(curTimestamp == lastTimestamp):
            curTimestamp = None
        else:
            curTimestamp = curTimestamp + datetime.timedelta(days=incrementInDays)
    return timestampToIntegerDict

def getFinalSequence(timestampsSorted,timestampToIntegerDict,timestampToEventDict):
    finalList = []
    for ts in timestampsSorted:
        i = timestampToIntegerDict[ts]
        for key in timestampToEventDict[ts]:
            finalList.append((i,key))
    return finalList


def main(algorithmType,dataFile):
    print("Starting Data Loading")
    # print(timestampToEventDict)
    timestampToEventDict = loadTimestampToEventDictFromFile(dataFile)
    timestampsSorted = sorted(timestampToEventDict.keys())
    timestampToIntegerDict = getTimestampToIntegerDict1DayIncrement(timestampsSorted)
    sequence = getFinalSequence(timestampsSorted, timestampToIntegerDict, timestampToEventDict)
    if(algorithmType == "WINEPI"):
        print("Starting WINEPI")
        alg = WINEPI(sequence, episode_type='serial')
        freqItems, suppData = alg.WinEpi(width=11, step=1, minFrequent=0.05)
        print("Done with WINEPI")
        winepiRules = WinEpiRules(freqItems, suppData, width=11, minConfidence=0.9)
        ruleList = winepiRules.generateRules()
        winepiRules.printRules(ruleList)
    elif (algorithmType == "MINEPI"):
        print("Starting MINEPI")
        alg = MINEPI(sequence, episode_type='serial')
        freqEpisodes = alg.MinEpi(max_width=11, step=1, minFrequent=0.05)
        print("Done with MINEPI")
        minepiRules = MinEpiRules(freqEpisodes, max_width=11, step=1, minConfidence=0.9)
        ruleList = minepiRules.generateRules()
        minepiRules.printRules(ruleList)
    else:
        print("Unknown algorithm type")
    print("Done with Everything")

if __name__ == "__main__":
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))
    algorithmType = sys.argv[1]
    dataFile = sys.argv[2]
    start = timeit.default_timer()
    main(algorithmType, dataFile)
    stop = timeit.default_timer()
    print('Total Time: ', stop - start)
