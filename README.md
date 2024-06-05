Last updated: 05/06/2024
# LOL-V2
This is my personal project about League of Legends and is an improved version from the previous ones as I will be doing the data gathering by myself using the Riot API. The main goal of this project is to analyze the data and create a model that can predict the outcome of a match based on the data gathered.

# Reason
League of Legends is a game that I have been playing for a long time (approximately ~ 10 years) and I have always been interested in the data that the game provides. I have always wanted to create a model that can predict the outcome of a match based on the data that the game provides. This project is a way for me to learn more about data analysis and machine learning.

Although there were already some datasets available online, this is still an online game. Hence, the data is constantly changing and I wanted to have the most up-to-date data possible. This is why I decided to gather the data myself using the Riot API. 

With that being said, I'm sure that my data will be obsolete in a few months, but I will still want to give it a try.

# Data Gathering
In this project, I will be only using data from the highest tier of the game, which is Challenger and Grandmaster.

## encryptedSummonerID
The first step is to get the encryptedsummonerID of the players in the highest tier. As of right now, there are about 300 players in the Challenger tier and 700 players in the Grandmaster tier. I will be using the Riot API to get the summonerID of these players using this [API](https://developer.riotgames.com/apis#league-exp-v4). 

## PUUID
After getting the encryptedsummonerID, I will be using this [API](https://developer.riotgames.com/apis#summoner-v4) to get their respective PUUID.

## Match History
Next up, for each of these PUUIDs, we will be getting their match history using this [API](https://developer.riotgames.com/apis#match-v5/GET_getMatchIdsByPUUID) to get their latest 100 matches.

## Match Data
Because we are aiming for 15 minutes of data, we need to get the specific details of each math. We will be using this [API](https://developer.riotgames.com/apis#match-v5/GET_getTimeline) to get the data of each match.

### Features
| **Value**                | **Explanation**                                                                    | **Where/How to get**                                                                        |
|--------------------------|------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| win                      | Which team did win                                                                 | 'GAME_END'-event                                                                            |
| wardsPlaced              | A ward provides vision and might prevent death                                     | Iterate over each 'WARD_PLACED'-event and add up                                            |
| wardsDestroyed           |                                                                                    | Iterate over each 'WARD_KILL'-event and add up                                              |
| firstBlood               | The first kill in a game provides extra gold                                       | 'killType': 'KILL_FIRST_BLOOD'                                                              |
| kills                    | Provides gold and experience and prevents enemy from gathering gold and experience | Iterate over each 'type': 'CHAMPION_KILL' and add for each 'killerID'                       |
| deaths                   |                                                                                    | Iterate over each 'type': 'CHAMPION_KILL' and add for each 'victimID'                       |
| assists                  | Provides a tiny bit of gold and experience                                         | Iterate over each 'type': 'CHAMPION_KILL' and add 'assistingParticipantIds' for each player |
| dragons                  | Provides team-wide buff, gold and experience                                       | Iterate over each 'mosterType': 'DRAGON' and read 'killerTeamId'                            |
| heralds                  | Once killed, a herald can be placed to destroy buildings                           | Iterade over each 'monsterType': 'RIFTHERALD' and read 'killerTeamId'                       |
| towerDestroyed           | Provides gold, opens the map                                                       | Iterate over each 'type': 'BUILDING_KILL' where 'buildingType': 'TOWER_BUILDING'            |
| totalGold                | Gold is required to purchase items                                                 | Read 'totalGold' from 'stats' per player                                                    |
| avgLevel                 | Player get better stats when advancing to the next level                           | Read 'level' for each summoner and divide by 5                                              |
| totalMinionsKilled       | Minions provide gold and experience                                                | Read 'minionsKilled' and add up for each player                                             |
| totalJungleMonsterKilled | Jungle monster provide gold and experience                                         | Read 'jungleMinionsKilled' and add up for each player                                       |
| csPerMinute              | Amount of minions killed per minute                                                | Add totalMinionsKilled for each player, divide by 5, divide by 15                           |
| goldPerMinute            | Amount of gold acquired per minute                                                 | Read 'goldPerSecond' for each player, add up and divide by 5                                |
| gameDuration             |                                                                                    | 'GAME_END'-event                                                                            |