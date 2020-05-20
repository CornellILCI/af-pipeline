#!/usr/bin/Rscript
packages_root <- paste(Sys.getenv("EBSAF_ROOT"), "models/packages", sep='/')
##==================================================##
##==================================================##
##		Package: optparse		    ##
##==================================================##
##==================================================##
#dependencies of getopt (none, SUGGESTS: testthat)

#dependencies of optparse ([methods], getopt >= 1.20.2)
getOpt <- paste(packages_root, "getopt_1.20.2.tar.gz", sep="/") 
install.packages(getOpt, repos=NULL, type="source")

##==================================================##
optParse <- paste(packages_root, "optparse_1.6.1.tar.gz", sep="/")
install.packages(optParse, repos=NULL, type="source")
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
rOO <- paste(packages_root, "R.oo_1.22.0.tar.gz", sep="/")
install.packages(rOO, repos=NULL, type="source")
Rmethods <- paste(packages_root, "R.methodsS3_1.7.1.tar.gz", sep="/")
install.packages(Rmethods, repos=NULL, type="source")

##==================================================##
#dependencies of plyr (R >= 3.1.0, Rcpp)
Rcpp <- paste(packages_root, "Rcpp_1.0.0.tar.gz", sep="/")
install.packages(Rcpp, repos=NULL, type="source")

##==================================================##
#dependencies of PBTools
digger <- paste(packages_root, "DiGGer_0.2-31_R_x86_64-unknown-linux-gnu.tar.gz", sep="/")
install.packages(digger, repos=NULL, type="source")
plyr <- paste(packages_root, "plyr_1.8.4.tar.gz", sep="/")
install.packages(plyr, repos=NULL, type="source")

##==================================================##
pbTools <- paste(packages_root, "PBTools_2.0.0.tar.gz", sep="/")
install.packages(pbTools, repos=NULL, type="source")
##==================================================##
##end for Package: PBTools
##==================================================##
