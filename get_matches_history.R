library(httr2)
library(jsonlite)
library(readr)

riot_api_key <- read_file("riot_api_key.txt")
puuid_list <- read.table("puuid_list.txt", col.names = "puuid")

matches <- data.frame(gameId=character())

for ( i in 1:nrow(puuid_list) ) {
  print(paste0("Handling " , i))
  puuid <- puuid_list$puuid[i]
  url <- paste0("https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/", puuid, "/ids?start=0&count=100&api_key=", riot_api_key)
  request <- request(url)
  response <- req_perform(request)
  response <- resp_body_string(response)
  matches <- rbind(matches, data.frame(gameId=unlist(data)))
  Sys.sleep(1.3)
  print("Done")
}

write.table(matches, "matches.txt", row.names = FALSE, col.names = FALSE, append = TRUE)
