#!/usr/bin/Rscript
packages_root <- paste(Sys.getenv("EBSAF_ROOT"), "models/packages", sep='/')
##==================================================##
##==================================================##
##		Package: optparse		    ##
##==================================================##
##==================================================##

#dependencies of optparse ([methods], getopt >= 1.20.2)
getOpt <- paste(packages_root, "getopt_1.20.2.tar.gz", sep="/") 
install.packages(getOpt, repos=NULL, type="source")

optParse <- paste(packages_root, "optparse_1.6.4.tar.gz", sep="/")
install.packages(optParse, repos=NULL, type="source")
##==================================================##
##end for Package: optparse
##==================================================##

##==================================================##
##==================================================##
##		Package: agricolae		    ##  
##==================================================##
##==================================================##

#dependencies of agricolae (klaR,MASS, nlme,cluster,AlgDesign,graphics)

#dependencies of klaR (combinat, questionr)
#klaR <- paste(packages_root, "klaR_0.6-15.tar.gz", sep="/") 
#install.packages(klaR, repos=NULL, type="source")

#agricolae <- paste(packages_root, "agricolae_1.3-2.tar.gz", sep="/") 
#install.packages(agricolae, repos=NULL, type="source")

##==================================================##
##end for Package: agricolae
##==================================================##
  
##==================================================##
##==================================================##
##		Package: ebsRtools		    ##
##==================================================##
##==================================================##

ebsRtools <- paste(packages_root, "ebsRtools_0.2.0.tar.gz", sep="/") 
install.packages(ebsRtools, repos=NULL, type="source")

##==================================================##
##end for Package: ebsRtools
##==================================================##