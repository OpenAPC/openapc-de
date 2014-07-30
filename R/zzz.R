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
my.df <- my.df[!is.na(my.df$doi),]

tt.doi <- ldply(my.df$doi, doi_fetch)

# transform:

my.df <- rbind(unireg, unibi)


#publisher title
my.df <- transform(my.df, 
          Publisher=ifelse(my.df$doi %in% tt.doi$doi, 
                                  as.character(tt.doi$publisher), 
                                  as.character(my.df$Publisher)))

# transform journal title

my.df <- transform(my.df, 
                   Journal=ifelse(my.df$doi %in% tt.doi$doi, 
                                    as.character(tt.doi$journal), 
                                    as.character(my.df$Journal)))
# issn.1

my.df <- transform(my.df, 
                   issn.1=ifelse(my.df$doi %in% tt.doi$doi, 
                                  as.character(tt.doi$ISSN.1), 
                                  as.character(my.df$issn.1)))

# issn.2

my.df <- transform(my.df, 
                   issn.2=ifelse(my.df$doi %in% tt.doi$doi, 
                                  as.character(tt.doi$ISSN.2), 
                                  as.character(my.df$issn.2)))

# map values

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

my.df <- read.csv("data/apc_de.csv", header =T, sep=",")
# dimension uni --> publisher
tt<- melt(tapply (my.df$EURO, list (my.df$uni, my.df$Publisher), sum))
tt <- tt[!is.na(tt$value),]
colnames(tt) <- c("source", "target", "value")

# join with apc per article set
apc <- my.df[, c("Publisher", "Journal", "EURO")]
colnames(apc) <- c("source", "target", "value")

apc <- rbind(apc, tt)

require(rCharts)
sankeyPlot <- rCharts$new()
sankeyPlot$setLib('http://timelyportfolio.github.io/rCharts_d3_sankey')

sankeyPlot$set(
  data = tt,
  nodeWidth = 10,
  nodePadding = 10,
  layout = 32,
  width = 960,
  height = 800,
  unit = "EURO",
  title= "Author fees paid by Bielefeld University Publication Fund 2012-13"
)
sankeyPlot

# sankey by uni regensburg

unireg <- my.df[my.df$uni == "Uni Regensburg",]

#select columns
unireg <- unireg[,c("Publisher", "Journal", "EURO")]

#rename
colnames(unireg) <- c("source", "target", "value")
unireg$value <- as.numeric(unireg$value)

#get affiliation 
tt <- as.data.frame(as.matrix((tapply(unireg$value,unireg$source, sum))))
tt$target <- rownames(tt)
tt$source <- rep("Uni Regensburg", times = nrow(tt))
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