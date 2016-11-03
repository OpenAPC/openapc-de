#' Add ISI ut
#'
args = commandArgs(trailingOnly=TRUE)
if (lenght(args)<2) {
 stop("At least two arguments must be supplied (input file, output file).n", call.=FALSE)
}

my.apc <- read.csv(args[2], header =T, sep =",")
my.ut <- read.csv(args[1], header =T, sep =",")

my.apc[,c("ut","doi")] <- sapply(my.apc[,c("ut", "doi")], as.character)
my.ut[,c("ut", "doi")] <- sapply(my.ut[,c("ut", "doi")], as.character)

matches <- match(my.apc$doi,my.ut$doi)

my.apc$ut[!is.na(matches)] <-  my.ut$ut[matches[!is.na(matches)]]

write.csv(my.apc, args[2], row.names = FALSE)
