import json
from mpyq import MPQArchive

from os import listdir
from colorama import init
from termcolor import colored

init()

def winners(filepath):
    archive = MPQArchive(str(filepath))
    files = archive.extract()
    data = json.loads(files[b"replay.gamemetadata.json"])
#     print(data)
    result_by_playerid = {p["PlayerID"]: p["Result"] for p in data["Players"]}
#     print(data["Players"])
#     print(result_by_playerid)
    return {
        playerid: result == "Win" for playerid, result in result_by_playerid.items()
}

# winners("./replays/MyBot_vs_DefaultRandomHard_DreamcatcherLE_11_05_063.SC2Replay")

directoryA = "./replays/testA/"
directoryB = "./replays/testB/"

totalgamesA = 0
wingamesA = 0

resultListA = []

for file in listdir("./replays/testA/"):
        totalgamesA += 1
        result = winners(directoryA+file)
        if result[1] == True:
                wingamesA += 1
                mybotresult = colored('victory', 'green')
        else:
                mybotresult = colored('defeat ', 'red')

        if result[2] == True: 
                defaultbotresult = colored('victory', 'green')
        else:
                defaultbotresult = colored('defeat', 'red')
        
        # print("MyBot:", mybotresult, ", Terran Easy:", defaultbotresult)
        resultString = "MyBot:" + mybotresult + ", Terran Easy:" + defaultbotresult + "|"
        # print(resultString)
        resultListA.append("MyBot:" + mybotresult + ", Terran Easy:" + defaultbotresult + "|")
        # print(result)

resultListA.append('Win Ratio:' + '{:.1%}'.format(wingamesA/totalgamesA) + '                  |')

# for resultString in resultListA:
#         print(resultString)

resultListB = []

totalgamesB = 0
wingamesB = 0

for file in listdir("./replays/testB/"):
        totalgamesB += 1
        result = winners(directoryB+file)
        if result[1] == True:
                wingamesB += 1
                mybotresult = colored('victory', 'green')
        else:
                mybotresult = colored('defeat ', 'red')

        if result[2] == True: 
                defaultbotresult = colored('victory', 'green')
        else:
                defaultbotresult = colored('defeat', 'red')
        
        resultString = "MyBot:" + mybotresult + ", Terran Easy:" + defaultbotresult
        # print(resultString)
        resultListB.append(resultString)

resultListB.append('Win Ratio:' + '{:.1%}'.format(wingamesB/totalgamesB))

for resultStringA, resultStringB in zip(resultListA, resultListB):
        print(resultStringA, resultStringB)