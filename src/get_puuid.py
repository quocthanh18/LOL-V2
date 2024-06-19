import requests
import time

riot_api_key = open("riot_api_key.txt", "r").read()

def main():
    s = requests.Session()
    with open("data/summonerID.txt") as f:
        summonerId = f.read().splitlines()
    with open("data/PUUID.txt", "a") as f:
        while len(summonerId) > 0:
            try:
                start = time.time()
                Id = summonerId[0]
                url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/{Id}?api_key={riot_api_key}"
                response = s.get(url).json()
                f.write(response["puuid"] + "\n")
                time.sleep(0.4)
                summonerId.pop(0)
                print(time.time() - start)
            except:
                print("Retrying in 1 secodns")
                time.sleep(1)

if __name__ == "__main__":
    main()