import json
from mpyq import MPQArchive

def winners(filepath):
    archive = MPQArchive(str(filepath))
    files = archive.extract()
    data = json.loads(files[b"replay.gamemetadata.json"])
    print(data)
    result_by_playerid = {p["PlayerID"]: p["Result"] for p in data["Players"]}
    print(data["Players"])
    print(result_by_playerid)
    return {
        playerid: result == "Win" for playerid, result in result_by_playerid.items()
}

winners("./replays/CrispZergRushBot_vs_DefaultTerranMedium_CatalystLE_08_42_014.SC2Replay")

