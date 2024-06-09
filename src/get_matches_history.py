import requests
import time
import pandas as pd

def main():
    riot_api_key = open("riot_api_key.txt", "r").read()
    puuid_list = list(pd.read_csv("data/puuid_list.txt"))
    for i in range(len(puuid_list)):
        url = f""
if __name__ == "__main__":
    main()