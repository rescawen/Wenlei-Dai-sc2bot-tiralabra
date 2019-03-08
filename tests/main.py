from os import listdir
from colorama import init

from directoryParser import parsingReplays

init()

def main():
        directoryA = "./replays/MyBot_EconomyOpener/Protoss_Elite/"
        directoryB = "./replays/MyBot_EconomyOpener/Terran_Elite/"
        directoryC = "./replays/MyBot_EconomyOpener/Zerg_Elite/"

        resultListA = parsingReplays(directoryA, 'Protoss Elite')
        resultListB = parsingReplays(directoryB, 'Terran Elite')
        resultListC = parsingReplays(directoryC, 'Zerg Elite')

        for resultStringA, resultStringB, resultStringC in zip(resultListA, resultListB, resultListC):
                print(resultStringA, resultStringB, resultStringC)
        
if __name__ == '__main__':
    main()


