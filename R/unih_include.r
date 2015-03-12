require(plyr)
require(RJSONIO)
require(RCurl)

unih <- read.csv("data/tuclaustahl/Grunddatei_Pubfonds.csv", header = TRUE, sep=",")

unih <- unih[!unih$DOI == "",]

source("R/doi_fetch.r")

tt.doi <- ldply(unih$DOI, doi_fetch)

#unih <- read.csv("data/fzj/FZJ2014.csv", header = TRUE, sep=",", dec = ",", na.strings = c("", "NA", "N/A"))
#data cleaning

# transform:
matches <- match(unih$DOI,tt.doi$doi)

# factor levels to character

unih[,c("Publisher","Journal", "ISSN.1", "ISSN.2")] <- 
  sapply(unih[,c("Publisher","Journal", "ISSN.1", "ISSN.2")], as.character)

#publisher
unih$Publisher[!is.na(matches)] <- as.character(tt.doi$publisher[matches[!is.na(matches)]])

#journal
unih$Journal[!is.na(matches)] <- as.character(tt.doi$journal[matches[!is.na(matches)]])

#issn
unih$ISSN.1[!is.na(matches)] <- as.character(tt.doi$ISSN.1[matches[!is.na(matches)]])

unih$ISSN.2[!is.na(matches)] <- as.character(tt.doi$ISSN.2[matches[!is.na(matches)]])

# manual clean up ambigue crossref publsiher and journal names 

unih$indexed_in_CrossRef <- unih$DOI %in% tt.doi$doi


# get pmid with rebi
require(devtools)
install_github("rebi", "njahn82")
library(rebi)

my.doi <- unih$DOI

my.pmc <- ldply(my.doi, function(x) search_publications(query = paste("doi:", x, sep="")))

my.pmc <- my.pmc[,c("pmid", "pmcid", "doi")]
#dirty handle NULL
my.pmc$pmcid <- as.character(my.pmc$pmcid)
my.pmc[my.pmc$pmcid == "NULL", "pmcid"] <- NA

my.pmc$pmid <- unlist(my.pmc$pmid)
my.pmc$doi <- unlist(my.pmc$doi)

unih <- droplevels(unih) 
my.tmp <- merge(unih, my.pmc, by.x="DOI", by.y="doi", all.x = T)

my.tmp$DOAJ <- TRUE
my.tmp$ut <- NA


# a bit of sorting

my.df <- my.tmp[,c("Institution", "Period", "Euro", "Publisher", 
                   "Journal", "ISSN.1", "ISSN.2", "DOI", 
                   "indexed_in_CrossRef","pmid", "pmcid", 
                   "base.url","record.id", "ut","DOAJ")]


my.all <- read.csv("data/apc_de.csv", header = T, sep =",")

my.df <- my.df[!my.df$DOI %in% my.all$doi,]
colnames(my.df) <- colnames(my.all)

my.all.t <- rbind(my.all, my.df)


doaj <- read.csv("data/doaj/doajJournalList.csv", header = T, sep = ",")
doaj.eissn <- doaj[!doaj$EISSN == "",] # exclude empty Eissn

# join ISSN and EISSN as vector
doaj.issn <- c(as.character(doaj$ISSN), as.character(doaj.eissn$EISSN))

# a bit of sorting

my.all.t$DOAJ <- !is.na(match(my.all.t$ISSN.1, doaj.issn) | match(my.all.t$ISSN.2, doaj.issn))

write.csv(my.all.t, "data/apc_de.csv", row.names = FALSE)

# make a sankey for hannover

unihan <- my.all[my.all$Institution == "Hannover U",]

#select columns
unihan <- unihan[,c("Publisher", "Journal", "EURO")]

#rename
colnames(unihan) <- c("source", "target", "value")
unihan$value <- as.numeric(unihan$value)

#get affiliation 
tt <- as.data.frame(as.matrix((tapply(unihan$value,unihan$source, sum))))
tt$target <- rownames(tt)
tt$source <- rep("Leibniz Universität Hannover", times = nrow(tt))
colnames(tt) <- c("value", "target", "source")

unihan.sub <- rbind(tt, unihan)


#now we finally have the data in the form we need
sankeyPlot <- rCharts$new()
sankeyPlot$setLib('http://timelyportfolio.github.io/rCharts_d3_sankey')

sankeyPlot$set(
  data = unihan.sub,
  nodeWidth = 15,
  nodePadding = 6,
  layout = 32,
  width = 960,
  height = 800,
  unit = "EURO",
  title= "Author fees paid by Leibniz Universität Hannover Publication Fund since 2013"
)
sankeyPlot