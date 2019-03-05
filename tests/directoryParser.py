from os import listdir
from termcolor import colored

from extractionFunction import extractResult

def parsingReplays(filepath):

    totalgames = 0
    wingames = 0
    resultList = []

    for file in listdir(filepath):

        totalgames += 1
        result = extractResult(filepath+file)
        
        if result[1] == True:
                wingames += 1
                mybotresult = colored('victory', 'green')
        else:
                mybotresult = colored('defeat ', 'red')

        if result[2] == True: 
                defaultbotresult = colored('victory', 'green')
        else:
                defaultbotresult = colored('defeat', 'red')
        
        resultList.append("MyBot:" + mybotresult + ", Terran Easy:" + defaultbotresult + "|")
        
    resultList.append('Win Ratio:' + '{:.1%}'.format(wingames/totalgames) + '                  |')

    return resultList