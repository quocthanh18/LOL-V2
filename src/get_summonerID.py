import requests
import time
import json
riot_api_key = open("riot_api_key.txt", "r").read()

def tier_crawler(tier):
    empty = False
    page = 1
    with open("data/summonerID.txt", "a") as f:
        while not empty:
            url = f"https://kr.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/{tier}/I?page={page}&api_key={riot_api_key}"
            response = requests.get(url).json()
            if not response:
                empty = True
                break
            else:
                for info in response:
                    f.write(info["summonerId"] + "\n")
            page += 1
            time.sleep(0.3)

def main():
    tier_crawler("CHALLENGER")    
    tier_crawler("GRANDMASTER")
if __name__ == "__main__":
    main()