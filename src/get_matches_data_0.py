import requests
import time
import csv

riot_api_key = "RGAPI-6c38614e-4f90-487e-b12e-353a569ded30"

def main():
    s = requests.Session()
    matches = open("data/batch_0.txt", "r").read().splitlines()
    matches = matches[matches.index("KR_7099894498") + 1: ]
    with open("data/batch_0_data.csv", "a") as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n") 
        counter = 0
        while len(matches) > 0:
            try:
                #Get match response
                matchId = matches[0]
                url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}/timeline?api_key={riot_api_key}"
                response = s.get(url)
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
                blueFirstTurret = 0
                blueInhibitorsDestroyed = 0
                blueFirstDragon = 0

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
                redFirstTurret = 0
                redInhibitorsDestroyed = 0
                redFirstDragon = 0

                gameDuration = 0
                #Check if the game is longer than 15.5 minutes
                lastEvent = data["info"]["frames"][-1]["events"][-1]
                if lastEvent["timestamp"] > 930000:
                    #blueWins
                    if lastEvent["winningTeam"] == 100:
                        blueWins = 1
                    
                    gameDuration = lastEvent["timestamp"] / 1000

                    minute = 0
                    checkFirstTurret = False
                    checkFirstDragon = False
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
                                        if not checkFirstDragon:
                                            blueFirstDragon = 1
                                            checkFirstDragon = True
                                    else:
                                        redDragons += 1
                                        if not checkFirstDragon:
                                            redFirstDragon = 1
                                            checkFirstDragon = True

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
                                
                            #Building
                            if event["type"] == "BUILDING_KILL":

                                #Towers
                                if event["buildingType"] == "TOWER_BUILDING":
                                    if event["killerId"] < 6:
                                        blueTowersDestroyed += 1
                                        if not checkFirstTurret:
                                            blueFirstTurret = 1
                                            checkFirstTurret = True
                                    else:
                                        redTowersDestroyed += 1
                                        if not checkFirstTurret:
                                            redFirstTurret = 1
                                            checkFirstTurret = True

                                #Inhibitors
                                if event["buildingType"] == "INHIBITOR_BUILDING":
                                    if event["killerId"] < 6:
                                        blueInhibitorsDestroyed += 1
                                    else:
                                        redInhibitorsDestroyed += 1

                            #Plates
                            if event["type"] == "TURRET_PLATE_DESTROYED":
                                if event["killerId"] < 6:
                                        bluePlatesDestroyed += 1
                                else:
                                        redPlatesDestroyed += 1

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
                        "blueFirstTurret": blueFirstTurret,
                        "blueInhibitorsDestroyed": blueInhibitorsDestroyed,
                        "blueFirstDragon": blueFirstDragon,

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
                        "redFirstTurret": redFirstTurret,
                        "redInhibitorsDestroyed": redInhibitorsDestroyed,
                        "redFirstDragon": redFirstDragon,

                        "gameDuration": gameDuration
                    }
                    writer.writerow(current_match_data.values())
                print("Match", matchId, "done")
                time.sleep(1.1)
                matches.pop(0)
            except KeyError:
                print("Retrying in 1 seconds")
                time.sleep(1)
            
            #Matches not found in the database
            #3 retries before moving on
                counter += 1
                if counter == 3:
                    matches.pop(0)
                    counter = 0
        

            
if __name__ == "__main__":
    main()
