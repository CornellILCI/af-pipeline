##==================================================##
##==================================================##
##		Package: optparse		    ##
##==================================================##
##==================================================##
#dependencies of getopt (none, SUGGESTS: testthat)

#dependencies of optparse ([methods], getopt >= 1.20.2)
install.packages("$PATH/packages/getopt_1.20.2.tar.gz", repos=NULL, type="source")

##==================================================##
install.packages("$PATH/packages/optparse_1.6.1.tar.gz", repos=NULL, type="source")
##==================================================##
##end for Package: optparse
##==================================================##


##==================================================##
##==================================================##
##		Package: PBTools		    ##
##==================================================##
##==================================================##
#dependencies of MASS (R >= 3.1.0, [grDevices], [graphics], [stats], [utils], Imports: [methods], Suggests: lattice, nlme, nnet, survival)
#dependencies of R.methodsS3 (R >= 2.13.0, [utils])
#dependencies of R.oo (R >= 2.13.0, R.methodsS3 (>= 1.7.1))
#dependencies of Rcpp (R >= 3.0.0, [methods], [utils])
##==================================================##
##==================================================##

#dependencies of DiGGer (R.oo, R.methodsS3, [MASS])
install.packages("$PATH/packages/R.oo_1.22.0.tar.gz", repos=NULL, type="source")
install.packages("$PATH/packages/R.methodsS3_1.7.1.tar.gz", repos=NULL, type="source")

##==================================================##
#dependencies of plyr (R >= 3.1.0, Rcpp)
install.packages("$PATH/packages/Rcpp_1.0.0.tar.gz", repos=NULL, type="source")

##==================================================##
#dependencies of PBTools
install.packages("$PATH/packages/DiGGer_0.2-31.tar.gz", repos=NULL, type="source")
install.packages("$PATH/packages/plyr_1.8.4.tar.gz", repos=NULL, type="source")

##==================================================##
install.packages("$PATH/packages/PBTools_2.0.0.tar.gz", repos=NULL, type="source")
##==================================================##
##end for Package: PBTools
##==================================================##