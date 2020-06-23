# -------------------------------------------------------------------------------------
# Name             : runALPHALATTICE
# Description      : Generate randomization and layout for Alpha Lattice Design which 
#                    can be run in the command line with arguments
# R Version        : 3.5.1 
# -------------------------------------------------------------------------------------
# Author           : Alaine A. Gulles 
# Author Email     : a.gulles@irri.org
# Date             : 2019.03.01
# Maintainer       : Alaine A. Gulles 
# Maintainer Email : a.gulles@irri.org
# Script Version   : 1
# -------------------------------------------------------------------------------------
# Parameters:
# nTreatment = number of entries
# nRep = number of replicates
# nBlk = number of blocks per replicate
# nTrial = number of trials (location rep)
# genLayout = logical; if TRUE, layout will be generated
# nFieldRow = number of field rows, required if genLayout is TRUE
# nRowPerRep = number of rows per replicate, required if genLayout is TRUE
# nRowPerBlk = number of rows per block, required if genLayout is TRUE
# serpentine = logical; if TRUE, plot numbers will be in serpentine arrangement, required if genLayout is TRUE
# outputFile = prefix to be used for the names of the output files
# outputPath = path where output will be saved
# ---------------------------------------------------------

suppressWarnings(suppressPackageStartupMessages(library(optparse)))
suppressWarnings(suppressPackageStartupMessages(library(PBTools)))

optionList <- list(
  make_option(opt_str = c("-n","--nTreatment"), type = "integer", default = NULL,
              help = "Number of entries", metavar = "number of entries"),
  make_option(opt_str = c("-r","--nRep"), type = "integer", default = NULL,
              help = "Number of replicates", metavar = "number of replicates"),
  make_option(opt_str = c("-b","--nBlk"), type = "integer", default = NULL,
              help = "Number of blocks", metavar = "number of blocks"),
  make_option(opt_str = c("-t","--nTrial"), default = as.integer(1),
              help = "Number of trials", metavar = "number of trials"),
  make_option(opt_str = c("--genLayout"), type = "logical", default = F,
              help = "Whether layout will be generated or not", metavar = "whether layout will be generated or not"),
  make_option(opt_str = c("--nFieldRow"), type = "integer", default = as.integer(1),
              help = "Number of field rows", metavar = "number of field rows"),
  make_option(opt_str = c("--nRowPerRep"), type = "integer", default = as.integer(1),
              help = "Number of rows per replicate", metavar = "number of rows per replicate"),
  make_option(opt_str = c("--nRowPerBlk"), type = "integer", default = as.integer(1),
              help = "Number of rows per block", metavar = "number of rows per block"),
  make_option(opt_str = c("--serpentine"), type = "logical", default = F,
              help = "Whether plot numbers will be in serpentine arrangement or not", metavar = "Whether plot numbers will be in serpentine arrangement or not"),
  make_option(opt_str = c("-o", "--outputFile"), type = "character", default = "RCBD_Expt",
              help = "Prefix to be used for the names of the output files",
              metavar = "prefix to be used for the names of the output files"),
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

# write the design information
sink(file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_designInfo.txt", sep = ""))
if (opt$genLayout) {
  temp <- try(result <- designAlphaLattice(generate = list(Entry = opt$nTreatment),
                                           numBlk = opt$nBlk,
                                           numRep = opt$nRep,
                                           numTrial = opt$nTrial,
                                           genLayout = opt$genLayout,
                                           numFieldRow = opt$nFieldRow,
                                           numRowPerRep = opt$nRowPerRep,
                                           numRowPerBlk = opt$nRowPerBlk,
                                           serpentine = opt$serpentine,
                                           display = TRUE),
              silent = TRUE)
} else {
  temp <- try(result <- designAlphaLattice(generate = list(Entry = opt$nTreatment),
                                           numBlk = opt$nBlk,
                                           numRep = opt$nRep,
                                           numTrial = opt$nTrial,
                                           genLayout = opt$genLayout,
                                           display = TRUE),
              silent = TRUE)
}

if(all(class(temp) == "try-error")) {
  msg <- trimws(strsplit(temp, ":")[[1]])
  msg <- trimws(paste(strsplit(msg, "\n")[[length(msg)]], collapse = " "))
  cat("Error in designAlphaLattice:", msg, sep = "")
}

sink()

if(all(class(temp) == "try-error")) { stop(paste("Error in designAlphaLattice:", msg, sep = "")) }

# save the fieldbook to a csv file
write.csv(result$fieldbook, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_fieldbook.csv", sep = ""), row.names = FALSE)

if (opt$genLayout) {
  for (i in (1:length(result$plan$TrmtLayout))) {
    temp <- result$plan$TrmtLayout[[i]]
    write.csv(temp, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_TrmtLayout_",names(result$plan$TrmtLayout)[i], ".csv", sep = ""))
  }
  
  for (i in 2:length(result$plan)) {
    write.csv(result$plan[[i]], file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_", names(result$plan)[i],".csv", sep = ""))
  }
} else {
  for (i in (1:length(unique(result$plan$TrmtLayout[,1])))) {
    tempTL <- result$plan$TrmtLayout[result$plan$TrmtLayout[,1] == unique(result$plan$TrmtLayout[,1])[i],]
    write.csv(tempTL, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_StatisticalDesignArray_", names(result$plan$TrmtLayout)[1], i, ".csv", sep = ""), row.names = FALSE)
    if (i == 1) {
      tempBL <- result$plan$BlockLayout[result$plan$BlockLayout[,1] == unique(result$plan$BlockLayout[,1])[i],]
      tempBL <- tempBL[,2:ncol(tempBL)]
      write.csv(tempBL, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_", names(result$plan)[2],".csv", sep = ""), row.names = FALSE)
    }
  }
  
}

