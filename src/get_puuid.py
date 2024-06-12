import requests
import time

riot_api_key = open("riot_api_key.txt", "r").read()

def main():
    with open("data/summonerID.txt") as f:
        summonerId = f.read().splitlines()
    with open("data/PUUID.txt", "a") as f:
        while len(summonerId) > 0:
            try:
                Id = summonerId[0]
                url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/{Id}?api_key={riot_api_key}"
                response = requests.get(url).json()
                f.write(response["puuid"] + "\n")
                time.sleep(0.5)
                summonerId.pop(0)
            except:
                print("Retrying in 1 secodns")
                time.sleep(1)

if __name__ == "__main__":
    main()