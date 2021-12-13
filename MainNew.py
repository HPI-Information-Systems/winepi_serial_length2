import json
import time
import datetime

from episode_mining.winepi import WINEPI, WinEpiRules

if __name__ == "__main__":
    sequence = sorted([
        (31, 'E'), (31, 'X'), (31, 'Y'), (31, 'Z'), (31, 'D'), (32, 'A'), (32, 'B'), (35, 'E'), (35, 'D'), (36, 'A'),
        (36, 'B'),
    ], key=lambda x: x[0])
    alg = WINEPI(sequence, episode_type='serial')
    freqItems, suppData = alg.WinEpi(width=3, step=1, minFrequent=0.1)
    winepiRules = WinEpiRules(freqItems, suppData, width=3, minConfidence=0.5)
    ruleList = winepiRules.generateRules()
    winepiRules.printRules(ruleList)
