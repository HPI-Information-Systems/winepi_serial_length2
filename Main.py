import json
import sys
import time
import datetime
import timeit

from episode_mining.minepi import MINEPI, MinEpiRules
from episode_mining.winepi import WINEPI, WinEpiRules

class Main():

    def __init__(self,algorithmType,dataFile,width,step,minSupport,minConfidence,timestampStepsInHours):
        self.algorithmType = algorithmType
        self.dataFile = dataFile
        self.width = int(width)
        self.step = int(step)
        self.minSupport = float(minSupport)
        self.minConfidence = float(minConfidence)
        self.timestampStepsInHours = int(timestampStepsInHours)

    def parseDateTime(self,x):
        if ('T' not in x):
            x = x + 'T0'
        return datetime.datetime.strptime(x, "%Y-%m-%dT%H")

    def loadTimestampToEventDictFromFile(self):
        file = open(dataFile)
        res = json.load(file)
        file.close()
        timestampToEventDict = {}
        keysSorted = sorted(res.keys())
        for i,key in enumerate(keysSorted):
            timestamps = sorted(list(map(lambda x: self.parseDateTime(x), res[key])))
            for ts in timestamps:
                eventList = timestampToEventDict.get(ts)
                if eventList is not None:
                    eventList.append(i)
                else:
                    newList = [i]
                    timestampToEventDict[ts] = newList
        return timestampToEventDict


    def getTimestampToIntegerDict(self, timestampsSorted):
        firstTimestamp = timestampsSorted[0]
        lastTimestamp = timestampsSorted[-1]
        # SOCRATA SPECIFIC: TODO - change this for Wikipedia!
        curTimestamp = firstTimestamp
        timestampToIntegerDict = {}
        curInteger = 0
        while curTimestamp != None:
            timestampToIntegerDict[curTimestamp] = curInteger
            curInteger += 1
            if (curTimestamp == lastTimestamp):
                curTimestamp = None
            else:
                curTimestamp = curTimestamp + datetime.timedelta(hours=self.timestampStepsInHours)
        return timestampToIntegerDict


    def getFinalSequence(self,timestampsSorted, timestampToIntegerDict, timestampToEventDict):
        finalList = []
        for ts in timestampsSorted:
            i = timestampToIntegerDict[ts]
            for key in timestampToEventDict[ts]:
                finalList.append((i, key))
        return finalList


    def main(self):
        print("Starting Data Loading")
        # print(timestampToEventDict)
        timestampToEventDict = self.loadTimestampToEventDictFromFile()
        timestampsSorted = sorted(timestampToEventDict.keys())
        timestampToIntegerDict = self.getTimestampToIntegerDict(timestampsSorted)
        sequence = self.getFinalSequence(timestampsSorted, timestampToIntegerDict, timestampToEventDict)
        if (self.algorithmType == "WINEPI"):
            print("Starting WINEPI")
            sys.stdout.flush()
            alg = WINEPI(sequence, episode_type='serial')
            freqItems, suppData = alg.WinEpi(width=self.width, step=self.step, minFrequent=self.minSupport)
            print("Done with WINEPI")
            winepiRules = WinEpiRules(freqItems, suppData, width=self.width, minConfidence=self.minConfidence)
            ruleList = winepiRules.generateRules()
            winepiRules.printRules(ruleList)
        elif (self.algorithmType == "MINEPI"):
            print("Starting MINEPI")
            sys.stdout.flush()
            alg = MINEPI(sequence, episode_type='serial')
            freqEpisodes = alg.MinEpi(max_width=self.width, step=self.step, minFrequent=self.minSupport)
            print("Done with MINEPI")
            minepiRules = MinEpiRules(freqEpisodes, max_width=self.width, step=self.step, minConfidence=self.minConfidence)
            ruleList = minepiRules.generateRules()
            minepiRules.printRules(ruleList)
        else:
            print("Unknown algorithm type")
        print("Done with Everything")


if __name__ == "__main__":
    print('Number of arguments:', len(sys.argv), 'arguments.')
    sys.stdout.flush()
    print('Argument List:', str(sys.argv))
    sys.stdout.flush()
    algorithmType = sys.argv[1]
    dataFile = sys.argv[2]
    width = sys.argv[3]
    step = sys.argv[4]
    minSupport = sys.argv[5]
    minConfidence = sys.argv[6]
    timestampStepsInHours = sys.argv[7]
    #width=11, step=1, minFrequent=0.05)
        #print("Done with WINEPI")
        #winepiRules = WinEpiRules(freqItems, suppData, width=11, minConfidence=0.9)
    start = timeit.default_timer()
    mainObject = Main(algorithmType,dataFile,width,step,minSupport,minConfidence,timestampStepsInHours)
    mainObject.main()
    stop = timeit.default_timer()
    print('Total Time: ', stop - start)
    sys.stdout.flush()
