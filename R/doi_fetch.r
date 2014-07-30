#' Helper function to retrieve metadata on CrossRef registered journal articles
#' 
#' @param x Digital Object Identifier (DOI) registered with CrossRef
#' @return data.frame containing info journal, publisher, doi and issn(s)
#' @require RJSONIO, RCurl
#' @details See \url{http://crosscite.org/cn/} for more info on DOI Content Negotiation.
#' 
#' @author Najko Jahn \email{najko.jahn@@uni-bielefeld.de}
#' 
#' @examples \dontrun{
#' doi_fetch("10.3389/fpsyg.2012.00519")
#' }


doi_fetch <- function(x) {  
  tt <- getURL(paste("http://data.crossref.org/", x, sep=""), 
               httpheader = c("Accept" = "application/vnd.citationstyles.csl+json"))
  
  if(tt == "Resource not found.") {
    warning(sprintf("There is no CrossRef citation matching your query: doi %s", x))
    tt.df = data.frame()
  } else {
    
    out <- fromJSON(tt)
    
    if(is.null(out)) {
      warning(sprintf("There is no citation matching your query: PMID %s", x))
      tt.df = data.frame()
    } else {
      #fields to parse
      doi <- out$doi
      csl.type <- out$type
      publisher <- out$publisher
      journal <- out$`container-title`
      ISSN.1 <- out$ISSN[1]
      ISSN.2 <- out$ISSN[2]
      
      tt.df <- data.frame(cbind(publisher, journal, ISSN.1, ISSN.2))
      
    }
    tt.df$doi <- x
  }
  return(tt.df)
}