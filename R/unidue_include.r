require(plyr)
require(RJSONIO)
require(RCurl)

unidue <- read.csv("data/unidue/unidue13.csv", header = TRUE, sep=",")

unidue.doi <- unidue[!is.na(unidue$doi),]

source("R/doi_fetch.r")

tt.doi <- ldply(unidue.doi$doi, doi_fetch, .inform = TRUE)

# transform:
matches <- match(unidue$doi,tt.doi$doi)

# factor levels to character

unidue[,c("Publisher","Journal")] <- sapply(unidue[,c("Publisher","Journal")], as.character)

#publisher
unidue$Publisher[!is.na(matches)] <- as.character(tt.doi$publisher[matches[!is.na(matches)]])

#journal
unidue$Journal[!is.na(matches)] <- as.character(tt.doi$journal[matches[!is.na(matches)]])

#issn
unidue$issn.1 <- as.character(unidue$issn.1)
unidue$issn.1[!is.na(matches)] <- as.character(tt.doi$ISSN.1[matches[!is.na(matches)]])
unidue$issn.2[!is.na(matches)] <- as.character(tt.doi$ISSN.2[matches[!is.na(matches)]])


# manual clean up ambigue crossref publsiher and journal names 

unidue$indexed_in_CrossRef <- unidue$doi %in% tt.doi$doi


# get pmid with rebi
require(devtools)
install_github("rebi", "ropensci")
library(rebi)

my.doi <- unidue$doi

my.pmc <- ldply(my.doi, function(x) search_publications(query = paste("doi:", x, sep="")))

my.pmc <- my.pmc[,c("pmid", "pmcid", "doi")]
#dirty handle NULL
my.pmc$pmcid <- as.character(my.pmc$pmcid)
my.pmc[my.pmc$pmcid == "NULL", "pmcid"] <- NA

my.pmc$pmid <- unlist(my.pmc$pmid)



my.tmp <- merge(unidue, my.pmc, by.x="doi", by.y="doi", all.x = T)

# emtpy columns

my.tmp$record.id <- NA
my.tmp$base.url <- NA
my.tmp$ut <- NA

# a bit of sorting

my.df <- my.tmp[,c("Institution", "Period", "EURO", "Publisher", 
                   "Journal", "issn.1", "issn.2", "doi", 
                   "indexed_in_CrossRef","pmid", "pmcid", 
                   "record.id", "base.url", "ut")]

my.all <- read.csv("data/apc_de.csv", header = T, sep =",")
my.all <- my.all[,-c(1:2)]

colnames(my.df) <- colnames(my.all)

my.all.t <- rbind(my.all, my.df)

write.csv(my.all.t, "data/apc_de.csv")

# make a sankey for hannover

uniduean <- my.df[my.df$uni == "Universität Duisburg-Essen",]

#select columns
uniduean <- uniduean[,c("Publisher", "Journal", "EURO")]

#rename
colnames(uniduean) <- c("source", "target", "value")
uniduean$value <- as.numeric(uniduean$value)

#get affiliation 
tt <- as.data.frame(as.matrix((tapply(uniduean$value,uniduean$source, sum))))
tt$target <- rownames(tt)
tt$source <- rep("Universität Duisburg-Essen", times = nrow(tt))
colnames(tt) <- c("value", "target", "source")

uniduean.sub <- rbind(tt, uniduean)


#now we finally have the data in the form we need
sankeyPlot <- rCharts$new()
sankeyPlot$setLib('http://timelyportfolio.github.io/rCharts_d3_sankey')

sankeyPlot$set(
  data = uniduean.sub,
  nodeWidth = 15,
  nodePadding = 10,
  layout = 32,
  width = 960,
  height = 800,
  unit = "EURO",
  title= "Author fees paid by Leibniz Universität Hannover Publication Fund since 2013"
)
sankeyPlot