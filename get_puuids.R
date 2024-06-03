library(httr2)
library(jsonlite)
library(readr)

riot_api_key <- "RGAPI-48b41f17-7fac-45aa-a8e5-0db90021b1e9"

summoner_names <- read.table("summonerId.txt", col.names = "SummonerID")
puuid_list <- data.frame(puuid=character())

for ( i in 1:nrow(summoner_names) ) {
  summoner_id <- summoner_names$SummonerID[i]
  url <- paste0("https://kr.api.riotgames.com/lol/summoner/v4/summoners/", summoner_id, "?api_key=", riot_api_key)
  request <- request(url)
  response <- req_perform(request)
  response <- resp_body_string(response)
  data <- fromJSON(response)
  puuid_list <- rbind(puuid_list, data.frame(puuid=data$puuid))
  Sys.sleep(1.3)
}
puuid_list <- do.call(data.frame, puuid_list)
write.table(puuid_list, "puuid_list.txt", row.names = FALSE, col.names = FALSE, append = TRUE)
  