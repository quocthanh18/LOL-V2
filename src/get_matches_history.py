import requests
import time
from concurrent.futures import ThreadPoolExecutor

riot_api_key = open("riot_api_key.txt", "r").read()
def main():
    puuid_list = open("data/PUUID.txt", "r").read().splitlines()
    matches = set()
    s = requests.Session()
    with open("data/matches_history.txt", "a") as f:
        while len(puuid_list) > 0:
            try:
                puuid = puuid_list[0]
                url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?queue=420&type=ranked&start=0&count=100&api_key={riot_api_key}"
                response = s.get(url).json()
                matches.update(list(response))
                time.sleep(0.5)
                puuid_list.pop(0)
                print(f"Player {puuid} done")
            except:
                print("Retrying")
                time.sleep(2)
        f.write("\n".join(matches))
            


if __name__ == "__main__":
    main()