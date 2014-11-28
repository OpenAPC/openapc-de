#' Add ISI ut
#' 

my.apc <- read.csv("data/apc_de.csv", header =T, sep =",")
my.ut <- read.csv("data/doi_ut.csv", header =T, sep =",")

matches <- match(my.apc$doi,my.ut$doi)

my.apc$ut[!is.na(matches)] <-  my.ut$ut[matches[!is.na(matches)]]

write.csv(my.apc, "data/apc_de.csv")
