import json
from mpyq import MPQArchive

def extractResult(filepath):
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