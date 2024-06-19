import requests
import time
riot_api_key = open("riot_api_key.txt", "r").read()
matches = open("data/matches_history.txt", "r").read().splitlines()


if __name__ == "__main__":
    s = requests.Session()
    with open("data/filtered__matches.txt", "a") as f:
        counter = 0
        while len(matches) > 0:
            try:
                matchId = matches[0]
                url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={riot_api_key}"
                response = s.get(url)
                data = response.json()["info"]
                metadata = []
                metadata.append(matchId)
                metadata.append(data["gameMode"])
                metadata.append(data["gameType"])
                metadata.append(data["teams"][0]["win"])
                metadata.append(data["teams"][1]["win"])
                f.write(str(metadata) + "\n")
                time.sleep(1.3)
                print(f"Match {matchId} done")
                matches.pop(0)
            except:
                print("Retrying")
                time.sleep(1)
                counter += 1
                if counter == 3:
                    counter = 0
                    matches.pop(0)


