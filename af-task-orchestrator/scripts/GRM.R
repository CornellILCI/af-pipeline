calcGenomicRelationshipMatrix <- function(locusMat){
  freq <- colMeans(locusMat) / 2
  locusMat <- scale(locusMat, center=TRUE, scale=F)
  return(tcrossprod(locusMat) / sum(2*freq*(1-freq)))
}