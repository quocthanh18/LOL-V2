library(httr2)
library(jsonlite)

riot_api_key <- read_file("riot_api_key.txt")
matches <- read.table("data/matches.txt", col.name="matchId")

matches_data <- data.frame()

for ( i in 1:5) {
  matchId <- matches[i, 1]
  print(paste0("Handling ", i ))
  url <- paste0("https://asia.api.riotgames.com/lol/match/v5/matches/", matchId, "/timeline?api_key=", riot_api_key)
  request <- request(url)
  response <- req_perform(request)
  response <- resp_body_string(response)
  data <- fromJSON(response) 
  blueWins <- 0
  
  blueWardsPlaced <- 0
  blueWardsDestroyed <- 0
  blueFirstBlood <- 0
  blueKills <- 0
  blueDeaths <- 0
  blueAssists <- 0
  blueDragons <- 0
  blueHeralds <- 0
  blueTowersDestroyed <- 0
  blueAvgLevel <- 0
  blueTotalExperience <- 0
  blueTotalMinionsKilled <- 0
  blueTotalJungleMinionsKilled <- 0
  blueCSPerMin <- 0
  blueGoldPerMin <- 0
  blueVoidGrubs <- 0
  bluePlates <- 0
  blueControlWardsPlaced <- 0
  blueControlWardsDestroyed <- 0
  
  redWardsPlaced <- 0
  redWardsDestroyed <- 0
  redFirstBlood <- 0
  redKills <- 0
  redDeaths <- 0
  redAssists <- 0
  redDragons <- 0
  redHeralds <- 0
  redTowersDestroyed <- 0
  redAvgLevel <- 0
  redTotalExperience <- 0
  redTotalMinionsKilled <- 0
  redTotalJungleMinionsKilled <- 0
  redCSPerMin <- 0
  redGoldPerMin <- 0
  redVoidGrubs <- 0
  redPlates <- 0
  redControlWardsPlaced <- 0
  redControlWardsDestroyed <- 0

  #test <- data$info$frames
  #rows <- nrow(test)
  #test1 <- as.data.frame(test[rows, 1])
  #rows2 <- nrow(test1)

  Frames <- as.data.frame(data$info$frames) 
  lastFrames <- Frames[nrow(Frames), ]
  
  Events <- as.data.frame(lastFrames$events)
  lastEvents <- Events[nrow(Events), ]
  
  if ( lastEvents[, "timestamp"] > 930000) {
    if ( lastEvents[, "type"] == "CHAMPION_KILL") {
      if ( lastEvents[, "winningTeam"] == 100) {
        blueWins <- 1
      }
      else {
        blueWins <- 0
      }
    }
    
    gameDuration <- lastEvents[, "timestamp"] / 1000
    
    minute <- 0
    
    while ( minute <= 15 ) {
      events <- as.data.frame(Frames[minute, "events"])
      
      for ( j in 1:nrow(events)) {
        
        #Wards Placed
        if ( events[j, "type"] == "WARD_PLACED") {
          if ( events[j, "creatorId"] <= 5 & events[j, "creatorId"] >= 1) {
            blueWardsPlaced <- blueWardsPlaced + 1
            if ( events[j, "wardType"] == "CONTROL_WARD") {
              blueControlWardsPlaced <- blueControlWardsPlaced + 1
            }
          }
          else {
            if ( events[j, "wardType"] == "CONTROL_WARD") {
              redControlWardsPlaced <- blueControlWardsPlaced + 1
            }
            redWardsPlaced <- redWardsPlaced + 1
          }
        }
      
        #Wards Destroyed
        if ( events[j, "type"] == "WARD_KILLED") {
          if ( events[j, "killerId"] <= 5 & events[j, "killerId"] >= 1) {
            blueWardsDestroyed <- blueWardsDestroyed + 1
            if ( events[j, "wardType"] == "CONTROL_WARD") {
              blueControlWardsDestroyed <- blueControlWardsDestroyed + 1
            }
          }
          else {
            if ( events[j, "wardType"] == "CONTROL_WARD") {
              redControlWardsDestroyed <- redControlWardsDestroyed + 1
            }
            redWardsDestroyed <- redWardsDestroyed + 1
          }
        }
        
        #First Blood
        if ( events[j, "killType"] == "KILL_FIRST_BLOOD") {
          if ( events[j, "killerId"] <= 5 & events[j, "killerId"] >= 1) {
            blueFirstBlood <- 1
          }
          else {
            redFirstBlood <- 1
          }
        }
        
        #Kills/Deaths
        if ( events[j, "type"] == "CHAMPION_KILL") {
          if ( events[j, "killerId"] <= 5 & events[j, "killerId"] >= 1) {
            blueKills <- blueKills + 1
            redDeaths <- redDeaths + 1
            
            #Assists
            if ( !is.null(events[j, "assistingParticipantIds"])) {
              blueAssists <- blueAssists + length(events[j, "assistingParticipantIds"])
            }
          }
          else {
            redKills <- redKills + 1
            blueDeaths <- blueDeaths + 1
            
            #Assists
            if ( !is.null(events[j, "assistingParticipantIds"])) {
              redAssists <- redAssists + length(events[j, "assistingParticipantIds"])
            }
          }
        }
        
        #Dragons
        if ( events[j, "type"] == "ELITE_MONSTER_KILL") {
          if ( events[j, "monsterType"] == "DRAGON") {
            if ( events[j, "killerId"] <= 5 & events[j, "killerId"] >= 1) {
              blueDragons <- blueDragons + 1
            }
            else {
              redDragons <- redDragons + 1
            }
          }
        }
        
        #Heralds
        if ( events[j, "type"] == "ELITE_MONSTER_KILL") {
          if ( events[j, "monsterType"] == "RIFT_HERALD") {
            if ( events[j, "killerId"] <= 5 & events[j, "killerId"] >= 1) {
              blueHeralds <- blueHeralds + 1
            }
            else {
              redHeralds <- redHeralds + 1
            }
          }
        }
        
        #Void grubs
        if ( events[j, "type"] == "ELITE_MONSTER_KILL") {
          if ( events[j, "monsterType"] == "HORDE") {
            if ( events[j, "killerId"] <= 5 & events[j, "killerId"] >= 1) {
              blueVoidGrubs <- blueVoidGrubs + 1
            }
            else {
              redVoidGrubs <- redVoidGrubs + 1
            }
          }
        }
        
        #Towers Destroyed
        if ( events[j, "type"] == "BUILDING_KILL") {
          if ( events[j, "buildingType"] == "TOWER_BUILDING") {
            if ( events[j, "killerId"] <= 5 & events[j, "killerId"] >= 1) {
              blueTowersDestroyed <- blueTowersDestroyed + 1
            }
            else {
              redTowersDestroyed <- redTowersDestroyed + 1
            }
          }
        }
        
        
      }
    }
      minute <- minute + 1
  }
    
}


