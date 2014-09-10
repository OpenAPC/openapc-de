require(plyr)
require(RJSONIO)
require(RCurl)

unih <- read.csv("data/unihannover//unihannover.csv", header = TRUE, sep=",")

source("R/doi_fetch.r")

tt.doi <- ldply(unih$DOI, doi_fetch)

# transform:
matches <- match(unih$DOI,tt.doi$doi)

# factor levels to character

unih[,c("Publisher","Journal")] <- sapply(unih[,c("Publisher","Journal")], as.character)

#publisher
unih$Publisher[!is.na(matches)] <- as.character(tt.doi$publisher[matches[!is.na(matches)]])

#journal
unih$Journal[!is.na(matches)] <- as.character(tt.doi$journal[matches[!is.na(matches)]])

#issn
unih$issn.1[!is.na(matches)] <- as.character(tt.doi$ISSN.1[matches[!is.na(matches)]])

unih$issn.2[!is.na(matches)] <- as.character(tt.doi$ISSN.2[matches[!is.na(matches)]])

# manual clean up ambigue crossref publsiher and journal names 

unih$indexed_in_CrossRef <- unih$DOI %in% tt.doi$doi


# get pmid with rebi
require(devtools)
install_github("rebi", "ropensci")
library(rebi)

my.doi <- unih$DOI

my.pmc <- ldply(my.doi, function(x) search_publications(query = paste("doi:", x, sep="")))

my.pmc <- my.pmc[,c("pmid", "pmcid", "doi")]
#dirty handle NULL
my.pmc$pmcid <- as.character(my.pmc$pmcid)
my.pmc[my.pmc$pmcid == "NULL", "pmcid"] <- NA

my.pmc$pmid <- unlist(my.pmc$pmid)



my.tmp <- merge(unih, my.pmc, by.x="DOI", by.y="doi", all.x = T)

# a bit of sorting

my.df <- my.tmp[,c("Institution", "Period", "EURO", "Publisher", 
                   "Journal", "ISSN.1", "ISSN.2", "DOI", 
                   "indexed_in_CrossRef","pmid", "pmcid", 
                   "record.id", "base.url")]

my.df$ut <- NA

my.all <- read.csv("data/apc_de.csv", header = T, sep =",")

colnames(my.df) <- colnames(my.all)

my.all.t <- rbind(my.all, my.df)

write.csv(my.all.t, "data/apc_de.csv")