unibi <- read.csv("data/unibi12-13.csv", header = T, sep =",")

unireg.12 <- read.csv("data/unireg12.csv", header = T, sep = ",")
unireg.13 <- read.csv("data/unireg13.csv", header = T, sep = ",")

unireg <- rbind(unireg.12, unireg.13)

unibi$base.url <- "http://pub.uni-bielefeld.de/"
unibi$uni <- "Uni Bielefeld"

unireg$base.url <- "http://epub.uni-regensburg.de/"
unireg$uni <- "Uni Regensburg"


colnames(unibi) <- c("repo_id", "EURO", "Period", "Publisher", "Journal", "doi", "issn.1", 
                      "issn.2", "base.url","uni")
colnames(unireg) <- c("repo_id", "EURO", "Period", "Publisher", "Journal", "doi", "issn.1", 
                      "issn.2", "base.url","uni")

my.df <- rbind(unireg, unibi)

# disambiguate journal, publisher names 

require(plyr)
require(RCurl)
require(RJSONIO)

source("R/doi_fetch.r")

# exclude empy
my.doi.na <- my.df[!is.na(my.df$doi),]

tt.doi <- ldply(my.doi.na$doi, doi_fetch)

# transform:
matches <- match(my.df$doi,tt.doi$doi)

# factor levels to character

my.df[,c("Publisher","Journal")] <- sapply(my.df[,c("Publisher","Journal")], as.character)

#publisher
my.df$Publisher[!is.na(matches)] <- as.character(tt.doi$publisher[matches[!is.na(matches)]])

#journal
my.df$Journal[!is.na(matches)] <- as.character(tt.doi$journal[matches[!is.na(matches)]])

#issn
my.df$issn.1[!is.na(matches)] <- as.character(tt.doi$ISSN.1[matches[!is.na(matches)]])

my.df$issn.2[!is.na(matches)] <- as.character(tt.doi$ISSN.2[matches[!is.na(matches)]])

# manual clean up ambigue crossref publsiher and journal names 

my.df$Publisher <-  mapvalues(my.df$Publisher,  "OMICs Publ. Group",
                              "OMICS Publishing Group")
my.df$Journal <- mapvalues(my.df$Journal, c("Frontiers in Psychology", "Frontiers in Plant Science" ), 
                           c("Front. Psychology", "Front. Plant Sci."))

# show for whichr ecords CrossRef metadata were used

my.df$indexed_in_CrossRef <- my.df$doi %in% tt.doi$doi

# export

write.csv(my.df, "data/apc_de.csv")

# get pmid with rebi
require(devtools)
install_github("rebi", "ropensci")
library(rebi)

my.df.s <- my.df[!(is.na(my.df$doi)),] 
my.doi <- my.df.s$doi

my.pmc <- ldply(my.doi, function(x) search_publications(query = paste("doi:", x, sep="")))

my.pmc <- my.pmc[,c("pmid", "pmcid", "doi")]
#dirty handle NULL
my.pmc$pmcid <- as.character(my.pmc$pmcid)
my.pmc[my.pmc$pmcid == "NULL", "pmcid"] <- NA

my.pmc$pmid <- unlist(my.pmc$pmid)



my.tmp <- merge(my.df, my.pmc, by="doi", all.x = T)

# a bit of sorting

my.df <- my.tmp[,c("uni", "Period", "EURO", "Publisher", 
                   "Journal", "issn.1", "issn.2", "doi", 
                   "indexed_in_CrossRef","pmid", "pmcid", 
                   "repo_id", "base.url")]

write.csv(my.df, "data/apc_de.csv", row.names = FALSE)


# prepare sankey
require(reshape)

my.df <- read.csv("data/apc_de.csv", header =T, sep=",")
# dimension uni --> publisher
tt<- melt(tapply (my.df$EURO, list (my.df$Institution, my.df$Publisher), sum))
tt <- tt[!is.na(tt$value),]
colnames(tt) <- c("source", "target", "value")

# # join with apc per article set
# apc <- my.df[, c("Publisher", "Journal", "EURO")]
# colnames(apc) <- c("source", "target", "value")

# apc <- rbind(apc, tt)

require(rCharts)
sankeyPlot <- rCharts$new()
sankeyPlot$setLib('http://timelyportfolio.github.io/rCharts_d3_sankey')

sankeyPlot$set(
  data = tt,
  nodeWidth = 40,
  nodePadding = 7,
  layout = 1,
  width = 600,
  height = 600,
  unit = "EURO",
  title= "Author fees paid by Bielefeld University and University of Regensburg Publication Fund 2012-13"
)
sankeyPlot

# sankey by uni regensburg

unireg <- my.df[my.df$Institution == "FZJ - ZB",]
unireg <- unireg[!is.na(unireg$doi),]
#select columns
unireg <- unireg[,c("Publisher", "Journal", "EURO")]

#rename
colnames(unireg) <- c("source", "target", "value")
unireg$value <- as.numeric(unireg$value)
 unireg <- droplevels(unireg)
#get affiliation 
tt <- as.data.frame(as.matrix((tapply(unireg$value,unireg$source, sum))))
tt$target <- rownames(tt)
tt$source <- rep("FZJ - ZB", times = nrow(tt))
colnames(tt) <- c("value", "target", "source")

unireg.sub <- rbind(tt, unireg)


#now we finally have the data in the form we need
sankeyPlot <- rCharts$new()
sankeyPlot$setLib('http://timelyportfolio.github.io/rCharts_d3_sankey')

sankeyPlot$set(
  data = unireg.sub,
  nodeWidth = 15,
  nodePadding = 10,
  layout = 32,
  width = 960,
  height = 800,
  unit = "EURO",
  title= "Author fees paid by University of Regensburg Publication Fund 2012-13"
)
sankeyPlot