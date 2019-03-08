from os import listdir
from colorama import init

from directoryParser import parsingReplays

init()

# not managing packages with pip so might have to install dependecies manually

def main():
        directoryA = "./replays/testA/"
        directoryB = "./replays/testB/"

        resultListA = parsingReplays(directoryA)
        resultListB = parsingReplays(directoryB)

        for resultStringA, resultStringB in zip(resultListA, resultListB):
                print(resultStringA, resultStringB)
        
if __name__ == '__main__':
    main()


