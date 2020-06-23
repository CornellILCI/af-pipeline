# -------------------------------------------------------------------------------------
# Name             : runAUGMENTEDRCBD
# Description      : Generate randomization and layout for Augmented Randomized  
#                    Complete Block Design which can be run in the command line with 
#                    arguments
# R Version        : 3.5.1 
# -------------------------------------------------------------------------------------
# Author           : Alaine A. Gulles 
# Author Email     : a.gulles@irri.org
# Date             : 2019.03.12
# Maintainer       : Alaine A. Gulles 
# Maintainer Email : a.gulles@irri.org
# Script Version   : 1
# -------------------------------------------------------------------------------------
# Parameters:
# nCheckTreatment = number of check or replicated entries
# nTestTreatment = number of test or unreplicated entries
# nRep = number of replicates (replicate_block)
# nTrial = number of trials (location rep)
# genLayout = logical; if TRUE, layout will be generated
# nFieldRow = number of field rows, required if genLayout is TRUE
# nRowPerRep = number of rows per replicate, required if genLayout is TRUE
# serpentine = logical; if TRUE, plot numbers will be in serpentine arrangement, required if genLayout is TRUE
# outputFile = prefix to be used for the names of the output files
# outputPath = path where output will be saved
# ---------------------------------------------------------

suppressWarnings(suppressPackageStartupMessages(library(optparse)))
suppressWarnings(suppressPackageStartupMessages(library(PBTools)))

optionList <- list(
  make_option(opt_str = c("--nCheckTreatment"), type = "integer", default = NULL,
              help = "Number of check entries", metavar = "number of check entries"),
  make_option(opt_str = c("--nTestTreatment"), type = "integer", default = NULL,
              help = "Number of test entries", metavar = "number of test entries"),
  make_option(opt_str = c("-r","--nRep"), type = "integer", default = NULL,
              help = "Number of replicates", metavar = "number of replicates"),
  make_option(opt_str = c("-t","--nTrial"), default = as.integer(1),
              help = "Number of trials", metavar = "number of trials"),
  make_option(opt_str = c("--genLayout"), type = "logical", default = F,
              help = "Whether layout will be generated or not", metavar = "whether layout will be generated or not"),
  make_option(opt_str = c("--nFieldRow"), type = "integer", default = as.integer(1),
              help = "Number of field rows", metavar = "number of field rows"),
  make_option(opt_str = c("--nRowPerRep"), type = "integer", default = as.integer(1),
              help = "Number of rows per replicate", metavar = "number of rows per replicate"),
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
  temp <- try(result <- designAugmentedRCB(numCheck = opt$nCheckTreatment, 
                                           numTest = opt$nTestTreatment, 
                                           trmtName = "Entry", 
                                           numBlk = opt$nRep, 
                                           numTrial = opt$nTrial,
                                           genLayout = opt$genLayout,
                                           numFieldRow = opt$nFieldRow,
                                           numRowPerBlk = opt$nRowPerRep,
                                           serpentine = opt$serpentine,
                                           display = TRUE), 
              silent = TRUE)
} else {
  temp <- try(result <- designAugmentedRCB(numCheck = opt$nCheckTreatment, 
                                           numTest = opt$nTestTreatment, 
                                           trmtName = "Entry", 
                                           numBlk = opt$nRep, 
                                           numTrial = opt$nTrial,
                                           genLayout = opt$genLayout,
                                           display = TRUE), 
              silent = TRUE) 
}

if(all(class(temp) == "try-error")) {
  msg <- trimws(strsplit(temp, ":")[[1]])
  msg <- trimws(paste(strsplit(msg, "\n")[[length(msg)]], collapse = " "))
  cat("Error in designAugmentedRCB:", msg, sep = "")
}

sink()

if(all(class(temp) == "try-error")) { stop(paste("Error in designAugmentedRCB:", msg, sep = "")) }

# rename the Block column
fbook <- result$fieldbook
names(fbook)[match("Block", names(fbook))] <- "Rep"

# save the fieldbook to a csv file
write.csv(fbook, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_fieldbook.csv", sep = ""), row.names = FALSE)

if (opt$genLayout) {
  names(result$plan)[3] <- "RepLayout"
  for (i in (1:length(result$plan$TrmtLayout))) {
    temp <- result$plan$TrmtLayout[[i]]
    write.csv(temp, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_TrmtLayout_",names(result$plan$TrmtLayout)[i], ".csv", sep = ""))
  }
  
  for (i in 2:length(result$plan)) {
    write.csv(result$plan[[i]], file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_", names(result$plan)[i],".csv", sep = ""))
  }
} else {
  for (i in (1:length(unique(result$plan[,1])))) {
    tempTL <- result$plan[result$plan[,1] == unique(result$plan[,1])[i],]
    
    # rename the Block column
    names(tempTL)[2:ncol(tempTL)] <- paste("Rep", 1:opt$nRep, sep = "")
    
    write.csv(tempTL, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_StatisticalDesignArray_", names(result$plan)[1], i, ".csv", sep = ""), row.names = FALSE)
  }
}

