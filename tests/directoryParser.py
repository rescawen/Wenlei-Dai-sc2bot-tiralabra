from os import listdir
from termcolor import colored

from extractionFunction import extractResult

# Going through each replay and creating string with the results of the game which is added into a list.
# For each directory we return a list. 

def parsingReplays(filepath, opponentName):

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
        
        resultList.append("MyBot:" + mybotresult + ", " + opponentName + ":" + defaultbotresult + "|")
        
    resultList.append('Win Ratio:' + '{:.1%}'.format(wingames/totalgames) + '                  |')

    return resultList