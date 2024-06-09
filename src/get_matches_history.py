import requests
import time

def main():
    riot_api_key = open("riot_api_key.txt", "r").read()
    puuid_list = open("data/PUUID.txt", "r").read().splitlines()
    with open("data/matches_history.txt", "a") as f:
        while len(puuid_list) > 0:
            try:
                puuid = puuid_list[0]
                url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start=0&count=100&api_key={riot_api_key}"
                response = requests.get(url).json()
                for match in response:
                    f.write(match + "\n")
                puuid_list.pop(0)
                time.sleep(0.5)
            except:
                print("Retrying in 2 seconds")
                time.sleep(0.5)


if __name__ == "__main__":
    main()