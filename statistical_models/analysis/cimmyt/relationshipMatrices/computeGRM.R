# -------------------------------------------------------------------------------------
# Name             : computeGRM
# Description      : Generates a Genomic Relationship Matrix from a marker matrix
# R Version        : 4.1.0
# -------------------------------------------------------------------------------------
# Author           : Pedro A M Barbosa
# Author Email     : p.medeiros@cgiar.org
# Date             : 2020.Ago.15
# Maintainer       : Pedro A M Barbosa
# Maintainer Email : p.medeiros@cgiar.org
# Script Version   : 1
# Syntax example   : "Rscript computeGRM.R -g genomicMatrix.csv"
# -------------------------------------------------------------------------------------
# Parameters:
# marker_matrix = csv file with the marker matrix. NxM matrix (N=ind,M=marker)
# ---------------------------------------------------------


# load the needed packages
suppressWarnings(suppressPackageStartupMessages(library(optparse)))
suppressWarnings(suppressPackageStartupMessages(library(AGHmatrix)))

optionList <- list(
  make_option(opt_str = c("-g","--genoMatrix"), type = "character", default = "genomicMatrix.csv",
              help = "name of the file with the marker matrix", metavar = "marker matrix file"),
  make_option(opt_str = c("-n","--ploidy"), type = "numeric", default = 2,
              help = "Ploidy of the species, data ploidy (an even number between 2 and 20).", metavar = "Crop ploidy"),
  make_option(opt_str = c("-m","--method"), type = "character", default = "VanRaden",
              help = "Method used to calculate GRM, VanRaden", metavar = ""),
  make_option(opt_str = c("-o", "--outputFile"), type = "character", default = "GRM_",
              help = "Prefix to be used for the names of the output files",
              metavar = "prefix to be used for the names of the output files"),
  make_option(opt_str = c("-v","--missingValue"), type = "character", default = "-9",
              help = "Signal in the matrix that codes a missing value", metavar = "missing value"),
  make_option(opt_str = c("-f","--maf"), type = "character", default = 0,
              help = "minimum allele frequency accepted to each marker", metavar = "minimum allele frequence"),
  make_option(opt_str = c("-p", "--outputPath"), type = "character", default = getwd(),
              help = "Path where output will be saved",
              metavar = "path where output will be saved")
)

# create an instance of a parser object
opt_parser = OptionParser(option_list = optionList)
opt = parse_args(opt_parser)

# check if folder is exist or not

if (!dir.exists(opt$outputPath)) {
  dir.create(opt$outputPath)
}

M <- read.csv(opt$genoMatrix, h = T,row.names = 1)
M <- as.matrix(M)

# randomization and write the design information in a txt file
sink(file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_GRM_Info.txt", sep = ""))
temp <- try(
  grm <- AGHmatrix::Gmatrix(M,
                            method=opt$method,
                            missingValue=opt$missingValue,
                            maf=opt$maf,
                            ploidy=opt$ploidy)
)

if(all(class(temp) == "try-error")) {
  msg <- trimws(strsplit(temp, ":")[[1]])
  msg <- trimws(paste(strsplit(msg, "\n")[[length(msg)]], collapse = " "))
  cat("Error in Gmatrix:", msg, sep = "")
}
sink()

if(all(class(temp) == "try-error")) { stop(paste("Error in generate GRM:", msg, sep = "")) }

# save grm in a csv file
write.csv(grm, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), ".csv", sep = ""), row.names = FALSE)
