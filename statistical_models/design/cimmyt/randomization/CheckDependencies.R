
######################################################################################
##
## File Name:  'CheckDependencies.R'
##
## Author:     FHRB Toledo  < f.toledo@cgiar.org >
##
## Local/Date: CIMMYT, Mexico / May 31th, 2020
##
## Source:     Check dependencies for packages within EBS
##
## Contents:   call to tools
##
##                                          ... several -- read comments (# ...)
##
##   `` Far better an approximate answer to the right question, which is often vague,
##      than the exact answer to the wrong question, which can always be
##      made precise ''   (John Tukey, Ann. Math. Stat. [33] 1962)
##
######################################################################################

## set relative path
setwd('../../../packages')

## packages in base distribution
base <- unname(installed.packages(priority = "base")[,1])

## packages in recommended distribution
reco <- unname(installed.packages(priority = 'recommended'))[,1]

## files in directory
files <- list.files()

## packages within directory
packages <- files[grepl('\\.tar\\.gz$', files)]

## packages names
names <- sub('\\_.*', '\\1', packages)

## check dependencies
tree <- tools::package_dependencies(packages = names)

## dependencies
deps <- unique(unname(unlist(tree)))

## packages out of directory
add <- deps[!(deps %in% unique(c(base, reco, names)))]

## check if packages need to be downloaded
if (length(add) != 0)
    stop(paste('\nPackage needs to be downloaded... :', add, '\n', collapse = ' '))

## \EOF
###########################################################################

