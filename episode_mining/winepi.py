# coding: utf-8
from numpy import *
import sys
from itertools import combinations, permutations
from . import WINEPIRule


class WINEPI(object):
    def __init__(self, sequence, episode_type='parallel'):
        self.sequence = sequence
        if episode_type not in ('serial', 'parallel'):
            raise Exception(
                '`episode_type` must be `serial` or `parallel`'
            )
        self.episode_type = episode_type
        # set up serial/parallel environment
        if episode_type == 'parallel':
            self.aprioriGen = self.aprioriGen_parallel
            self.scanWindows = self.scanWindows_parallel
        elif episode_type == 'serial':
            self.aprioriGen = self.aprioriGen_serial
            self.scanWindows = self.scanWindows_serial

    def slidingWindow(self):
        #first window:
        windows = [[self.sequence[0][1]]]
        t_end = self.sequence[0][0] + self.step
        t_start = t_end - self.width
        noWins = int((self.sequence[-1][0] - self.sequence[0][0] + self.width) / self.step)
        print("Generating windows between [0,", noWins - 1, ")")
        sequenceStartIndex=0
        for i in range(noWins - 1):  # because 1st window has been generated.
            print("Processing Window",i)
            window = []
            t_start += self.step;
            t_end += self.step
            t_current = t_start
            done=False
            curIndex=sequenceStartIndex
            while(not done and curIndex < len(self.sequence)):
                transaction = self.sequence[curIndex]
                if(t_start > transaction[0]):
                    sequenceStartIndex +=1
                if t_start <= transaction[0] and transaction[0] < t_end:
                    window.append(transaction[1])
                if transaction[0] >= t_end:
                    done=True
                curIndex+=1
            windows.append(window)
        return windows

    def createC1(self, windows):
        C1 = set()
        count = 0
        total = len(windows)
        for window in windows:
            print("Finished Window",count,"total:", total)
            sys.stdout.flush()
            count += 1
            for transaction in window:
                for item in transaction:
                    C1.add(item)
        C1List = list(map(lambda c: [c],list(C1)))
        C1List.sort()
        return C1List

    def scanWindows_parallel(self, windows, Ck):
        ssCnt = {}
        for tid in windows:
            for can in Ck:
                if set(can).issubset(tid):
                    # cannot use type 'set' in key of 'dictionary'
                    # so we use 'tuple' (Error: unhashable type)
                    if not tuple(can) in ssCnt:
                        ssCnt[tuple(can)] = 1
                    else:
                        ssCnt[tuple(can)] += 1
        numItems = float(len(windows))
        retList = []
        supportData = {}
        for key in ssCnt:
            support = ssCnt[key] / numItems
            if support >= self.minFrequent:
                retList.insert(0, key)
            supportData[key] = support
        return retList, supportData

    def isSubsetInOrderWithGap(self, sub, window):
        ln, j = len(sub), 0
        for transaction in window:
            if sub[j] in transaction:
                j += 1
            if j == ln:
                return True
        return False

    def scanWindows_serial(self, windows, Ck):
        ssCnt = {}
        print("Starting Serial Window Scan")
        sys.stdout.flush()
        windowCount = len(windows)
        count = 0
        for tid in windows:
            print("Starting Window", count, "Total:", windowCount)
            sys.stdout.flush()
            for can in Ck:
                if self.isSubsetInOrderWithGap(can, tid):
                    if not tuple(can) in ssCnt:
                        ssCnt[tuple(can)] = 1
                    else:
                        ssCnt[tuple(can)] += 1
            count += 1
        numItems = float(len(windows))
        retList = []
        supportData = {}
        for key in ssCnt:
            support = ssCnt[key] / numItems
            if support >= self.minFrequent:
                retList.insert(0, key)
            supportData[key] = support
        return retList, supportData

    def checkSubsetFrequency(self, candidate, Lk, k):
        if k > 1:
            subsets = list(combinations(candidate, k))
        else:
            return True
        for elem in subsets:
            if not elem in Lk:  # elem is tuple
                return False
        return True

    def aprioriGen_parallel(self, Lk, k):  # creates Ck
        resList = []  # result set
        candidatesK = []
        lk = sorted(set([item for t in Lk for item in t]))  # get and sort elements from frozenset
        candidatesK = list(combinations(lk, k))
        for can in candidatesK:
            if self.checkSubsetFrequency(can, Lk, k - 1):
                resList.append(can)
        return resList

    def aprioriGen_serial(self, Lk, k):  # creates Ck
        resList = []  # result set
        candidatesK = []
        lk = sorted(set([item for t in Lk for item in t]))  # get and sort elements from frozenset
        candidatesK = list(permutations(lk, k))
        for can in candidatesK:
            if self.checkSubsetFrequency(can, Lk, k - 1):
                resList.append(can)
        return resList

    def WinEpi(self, width, step, minFrequent):
        self.width = width
        self.step = step
        self.minFrequent = minFrequent
        windows = self.slidingWindow()
        print("Finished Window creation, beginning c1")
        sys.stdout.flush()
        C1 = self.createC1(windows)
        print("Finished C1 creation, beginning window scan")
        sys.stdout.flush()
        L1, supportData = self.scanWindows(windows, C1)
        print("Finished First Window scan, beginning k=2")
        sys.stdout.flush()
        L = [L1]
        k = 2
        while (k <= 2):
            print(k)
            sys.stdout.flush()
            Ck = self.aprioriGen(L[k - 2], k)
            print("Finished apriori Gen", k, "beginning window scan")
            sys.stdout.flush()
            Lk, supK = self.scanWindows(windows, Ck)  # scan DB to get Lk
            supportData.update(supK)
            L.append(Lk)
            k += 1
        # remove empty last itemset from L
        if L[-1] == []:
            L.pop()
        return L, supportData


class WinEpiRules(object):
    def __init__(self, largeItemSet, supportData, width, minConfidence):
        self.largeItemSet = largeItemSet
        self.supportData = supportData
        self.width = width
        self.minConf = minConfidence

    def generateRules(self):  # supportData is a dict coming from scanWindows_parallel
        bigRuleList = []
        for i in range(1, len(self.largeItemSet)):  # only get the sets with two or more items
            for item in self.largeItemSet[i]:  # for each item in a level
                for j in range(1, i + 1):  # i+1 equal to length of an item
                    lhsList = list(combinations(item, j))
                    for lhs in lhsList:  # lhs and item are both tuple
                        conf = self.supportData[item] / self.supportData[lhs]
                        if conf >= self.minConf:
                            bigRuleList.append(
                                WINEPIRule(list(lhs), list(item), self.width, self.supportData[item], conf))
        return bigRuleList

    def printRules(self, ruleList):
        for rule in ruleList:
            print(rule)
