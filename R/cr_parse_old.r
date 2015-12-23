#' Parse CrossRef TDM metadata
#' 
#' @import rcrossref
#' @param doi DOI

cr_parse_old <- function(doi) {
  
  tryCatch({
    doc <- rcrossref::cr_cn(doi, "crossref-tdm")
  }, error=function(err) {
    ## what to do on error? could return conditionMessage(err) or other...
    warning(sprintf("doi: %s not found", doi))
  })
  
  if(is.null(doc))
    return(NULL)
  else
    
    # namespaces
    nm = c(cr = "http://www.crossref.org/xschema/1.0",
           ct = "http://www.crossref.org/qrschema/3.0",
           ai = "http://www.crossref.org/AccessIndicators.xsd")
  
  #xpath queries
  xp_queries = c(doi = "//ct:doi",
                 journal_full_title = "//cr:journal_metadata//cr:full_title",
                 publisher = "//ct:crm-item[@name='publisher-name']",
                 issn = "//*[local-name() = 'journal_metadata']//*[local-name() = 'issn']",
                 issn_print = "//*[local-name() = 'journal_metadata']//*[local-name() = 'issn' and @media_type='print']",
                 issn_electronic = "//*[local-name() = 'journal_metadata']//*[local-name() = 'issn' and @media_type='electronic']",
                 license_ref = "//ai:license_ref")
  
  # sapply on xpath queries on nodes
  tt <- lapply(xp_queries, function(xp_queries) getNodeSet(doc, xp_queries, nm, xmlValue))
  # deal with empty list elements
  tt.df <- lapply(tt, function(x)  if (length(x) == 0) x <- NA  else x <- x)
  # deal with multiple value
  tt.df <- lapply(tt.df, function(x) if(length(x)>1) paste(x, collapse=";") else x <- x)
  # return vector
  unlist(tt.df)
}