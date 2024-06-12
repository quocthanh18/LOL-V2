import requests
import time

def main():
    riot_api_key = open("riot_api_key.txt", "r").read()
    puuid_list = open("data/PUUID.txt", "r").read().splitlines()
    with open("data/matches_history.txt", "a") as f:
        for puuid in puuid_list:
            url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&start=0&count=100&api_key={riot_api_key}"
            response = requests.get(url).json()
            for match in response:
                f.write(match + "\n")
            time.sleep(1)


if __name__ == "__main__":
    main()