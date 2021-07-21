# 2021.07.09
# Modified by JBonifacio from VUlat's installPackages.R script

packages_root <- paste(Sys.getenv("EBSAF_ROOT"), "models/packages", sep='/')

##==================================================##
##==================================================##
##		Package: optparse		    ##
##==================================================##
##==================================================##
install.packages("optparse")
##==================================================##
##end for Package: optparse
##==================================================##


##==================================================##
##==================================================##
##	     Package: PBToolsDesign		    ##
##==================================================##
##==================================================##
# dependencies of MASS (R >= 3.1.0, [grDevices], [graphics], [stats], [utils], Imports: [methods], Suggests: lattice, nlme, nnet, survival)
# dependencies of R.methodsS3 (R >= 2.13.0, [utils])
# dependencies of R.oo (R >= 2.13.0, R.methodsS3 (>= 1.7.1))
##==================================================##
##==================================================##

# dependencies of DiGGer (R.oo, R.methodsS3, [MASS])
Rmethods <- paste(packages_root, "R.methodsS3_1.8.1.tar.gz", sep="/")
install.packages(Rmethods, repos=NULL, type="source")
rOO <- paste(packages_root, "R.oo_1.24.0.tar.gz", sep="/")
install.packages(rOO, repos=NULL, type="source")

##==================================================##
#dependencies of PBToolsDesign (R >= 4.0.3, dplyr, crayon, DiGGer)
install.packages("dplyr")
install.packages("crayon")
digger <- paste(packages_root, "DiGGer_1.0.5.tgz", sep="/")
install.packages(digger, repos=NULL, type="source")

##==================================================##
pbTools <- paste(packages_root, "PBToolsDesign_2.1.0-21.07.09.tar.gz", sep="/")
install.packages(pbTools, repos=NULL, type="source")

##==================================================##
##end for Package: PBTools
##==================================================##
