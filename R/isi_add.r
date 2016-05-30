#' Add ISI ut
#'

my.apc <- read.csv("data/apc_de.csv", header =T, sep =",")
my.ut <- read.csv("apc_de_ut.csv", header =T, sep =",")

my.apc[,c("ut","doi")] <- sapply(my.apc[,c("ut", "doi")], as.character)
my.ut[,c("ut", "doi")] <- sapply(my.ut[,c("ut", "doi")], as.character)

matches <- match(my.apc$doi,my.ut$doi)

my.apc$ut[!is.na(matches)] <-  my.ut$ut[matches[!is.na(matches)]]

write.csv(my.apc, "data/apc_de.csv", row.names = FALSE)
