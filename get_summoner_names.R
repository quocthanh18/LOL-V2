library(httr2)
library(jsonlite)
library(tidyverse)

riot_api_key <- read_file("riot_api_key.txt")
page <- 1

summoner_crawler <- function(tier) {
  empty <- FALSE
  while ( !empty ) {
    url <- paste0("https://kr.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/", tier, "/I?page=", page, "&api_key=", riot_api_key)
    request <- request(url)
    response <- req_perform(request)
    response <- resp_body_string(response)
    data <- fromJSON(response)
    if (!is.null(data$summonerId)) {
      write.table(data$summonerId, "summonerId.txt", row.names = FALSE, col.names = FALSE, append = TRUE)
      page <- page + 1
    } else {
      empty <- TRUE
    }
    Sys.sleep(0.7)
  }

}

summoner_crawler("CHALLENGER")
summoner_crawler("GRANDMASTER")
