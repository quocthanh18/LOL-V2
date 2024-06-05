import requests
import time
import pandas as pd

def main():
    riot_api_key = open("riot_api_key.txt", "r").read()
    matches = pd.read_csv("data/matches.txt", names=["matchId"])
    matches_data = []
    for i in range(matches.shape[0]):
        #Get match response
        matchId = matches.loc[i, "matchId"]
        url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}/timeline?api_key={riot_api_key}"
        response = requests.get(url)
        data = response.json()

        #Features declaration
        blueWins = 0

        blueWardsPlaced = 0
        blueControlWardsPlaced = 0
        blueWardsDestroyed = 0
        blueControlWardsDestroyed = 0
        blueFirstBlood = 0
        blueKills = 0
        blueDeaths = 0
        blueAssists = 0
        blueDragons = 0
        blueHeralds = 0
        blueVoidGrubs = 0
        blueTowersDestroyed = 0
        bluePlatesDestroyed = 0
        blueTotalGold = 0
        blueTotalExperience = 0
        blueTotalMinionsKilled = 0
        blueTotalJungleMinionsKilled = 0
        blueCSPerMin = 0
        blueGoldPerMin = 0

        redWardsPlaced = 0
        redControlWardsPlaced = 0
        redWardsDestroyed = 0
        redControlWardsDestroyed = 0
        redFirstBlood = 0
        redKills = 0
        redDeaths = 0
        redAssists = 0
        redDragons = 0
        redHeralds = 0
        redVoidGrubs = 0
        redTowersDestroyed = 0
        redPlatesDestroyed = 0
        redTotalGold = 0
        redTotalExperience = 0
        redTotalMinionsKilled = 0
        redTotalJungleMinionsKilled = 0
        redCSPerMin = 0
        redGoldPerMin = 0

        gameDuration = 0
        #Check if the game is longer than 15 minutes
        lastEvent = data["info"]["frames"][-1]["events"][-1]
        if lastEvent["timestamp"] > 930000:
            #blueWins
            if lastEvent["winningTeam"] == 100:
                blueWins = 1
            
            gameDuration = lastEvent["timestamp"] / 1000

            minute = 0
            while minute <= 15:
                events_at_minute = data["info"]["frames"][minute]["events"]

                for event in events_at_minute:

                    #Wards placed
                    if event["type"] == "WARD_PLACED":
                            if event["creatorId"] < 6:
                                blueWardsPlaced += 1
                                if event["wardType"] == "CONTROL_WARD":
                                    blueControlWardsPlaced += 1
                            else:
                                redWardsPlaced += 1
                                if event["wardType"] == "CONTROL_WARD":
                                    redControlWardsPlaced += 1

                    #Wards destroyed
                    if event["type"] == "WARD_KILL":
                        if event["killerId"] < 6:
                            blueWardsDestroyed += 1
                            if event["wardType"] == "CONTROL_WARD":
                                blueControlWardsDestroyed += 1
                        else:
                            redWardsDestroyed += 1
                            if event["wardType"] == "CONTROL_WARD":
                                redControlWardsDestroyed += 1

                    
                    #First blood
                    if event["type"] == "CHAMPION_SPECIAL_KILL" and event["killType"] == "KILL_FIRST_BLOOD": 
                        if event["killerId"] < 6:
                                blueFirstBlood = 1
                        else:
                                redFirstBlood = 1

                    #Kills/Deaths
                    if event["type"] == "CHAMPION_KILL":
                        if event["killerId"] < 6:
                            blueKills += 1
                            redDeaths += 1
                            if "assistingParticipantIds" in event:
                                blueAssists += len(event["assistingParticipantIds"])
                        else:
                            redKills += 1
                            blueDeaths += 1
                            if "assistingParticipantIds" in event:
                                redAssists += len(event["assistingParticipantIds"])

                    #Neutral monsters
                    if event["type"] == "ELITE_MONSTER_KILL":

                        #Dragons
                        if event["monsterType"] == "DRAGON":
                            if event["killerId"] < 6:
                                blueDragons += 1
                            else:
                                redDragons += 1

                        #Heralds
                        if event["monsterType"] == "RIFTHERALD":
                            if event["killerId"] < 6:
                                blueHeralds += 1
                            else:
                                redHeralds += 1

                        #Void grubs
                        if event["monsterType"] == "HORDE":
                            if event["killerId"] < 6:
                                blueVoidGrubs += 1
                            else:
                                redVoidGrubs += 1
                        
                    #Towers 
                    if event["type"] == "BUILDING_KILL":
                        if event["killerId"] < 6:
                                redTowersDestroyed += 1
                        else:
                                blueTowersDestroyed += 1

                    #Plates
                    if event["type"] == "TURRET_PLATE_DESTROYED":
                        if event["killerId"] < 6:
                                redPlatesDestroyed += 1
                        else:
                                bluePlatesDestroyed += 1
                participants = data["info"]["frames"][minute]["participantFrames"]
                if 900000 < data["info"]["frames"][minute]["timestamp"] < 901000:
                    for participant in participants:
                        if int(participant) < 6:
                            blueTotalGold += participants[participant]["totalGold"]
                            blueTotalExperience += participants[participant]["xp"]
                            blueTotalMinionsKilled += participants[participant]["minionsKilled"]
                            blueTotalJungleMinionsKilled += participants[participant]["jungleMinionsKilled"]
                        else:
                            redTotalGold += participants[participant]["totalGold"]
                            redTotalExperience += participants[participant]["xp"]
                            redTotalMinionsKilled += participants[participant]["minionsKilled"]
                            redTotalJungleMinionsKilled += participants[participant]["jungleMinionsKilled"]
                minute += 1


            blueCSPerMin /= 15
            blueGoldPerMin /= 15

            redCSPerMin /= 15
            redGoldPerMin /= 15

            current_match_data = {
                "matchId": matchId,
                "blueWins": blueWins,
                "blueWardsPlaced": blueWardsPlaced,
                "blueControlWardsPlaced": blueControlWardsPlaced,
                "blueWardsDestroyed": blueWardsDestroyed,
                "blueControlWardsDestroyed": blueControlWardsDestroyed,
                "blueFirstBlood": blueFirstBlood,
                "blueKills": blueKills,
                "blueDeaths": blueDeaths,
                "blueAssists": blueAssists,
                "blueDragons": blueDragons,
                "blueHeralds": blueHeralds,
                "blueVoidGrubs": blueVoidGrubs,
                "blueTowersDestroyed": blueTowersDestroyed,
                "bluePlatesDestroyed": bluePlatesDestroyed,
                "blueTotalGold": blueTotalGold,
                "blueTotalExperience": blueTotalExperience,
                "blueTotalMinionsKilled": blueTotalMinionsKilled,
                "blueTotalJungleMinionsKilled": blueTotalJungleMinionsKilled,
                "blueCSPerMin": blueCSPerMin,
                "blueGoldPerMin": blueGoldPerMin,

                "redWardsPlaced": redWardsPlaced,
                "redControlWardsPlaced": redControlWardsPlaced,
                "redWardsDestroyed": redWardsDestroyed,
                "redControlWardsDestroyed": redControlWardsDestroyed,
                "redFirstBlood": redFirstBlood,
                "redKills": redKills,
                "redDeaths": redDeaths,
                "redAssists": redAssists,
                "redDragons": redDragons,
                "redHeralds": redHeralds,
                "redVoidGrubs": redVoidGrubs,
                "redTowersDestroyed": redTowersDestroyed,
                "redPlatesDestroyed": redPlatesDestroyed,
                "redTotalGold": redTotalGold,
                "redTotalExperience": redTotalExperience,
                "redTotalMinionsKilled": redTotalMinionsKilled,
                "redTotalJungleMinionsKilled": redTotalJungleMinionsKilled,
                "redCSPerMin": redCSPerMin,
                "redGoldPerMin": redGoldPerMin,

                "gameDuration": gameDuration
            }
            matches_data.append(current_match_data)
            print("Match", i, "done")
            time.sleep(1.4)

    matches_data = pd.DataFrame(matches_data)
    matches_data.to_csv("data/matches_data.csv", index=False)
            
if __name__ == "__main__":
    main()