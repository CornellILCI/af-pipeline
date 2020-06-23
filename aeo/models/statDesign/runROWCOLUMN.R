# -------------------------------------------------------------------------------------
# Name             : runROWCOLUMN
# Description      : Generate randomization and layout for Row-Column Design which 
#                    can be run in the command line with arguments
# R Version        : 3.5.1 
# -------------------------------------------------------------------------------------
# Author           : Alaine A. Gulles 
# Author Email     : a.gulles@irri.org
# Date             : 2019.03.05
# Maintainer       : Alaine A. Gulles 
# Maintainer Email : a.gulles@irri.org
# Script Version   : 1
# -------------------------------------------------------------------------------------
# Parameters:
# nTreatment = number of entries
# nRowBlk = number of blocks per replicate
# nRep = number of replicates
# nTrial = number of trials (location rep)
# genLayout = logical; if TRUE, layout will be generated
# nFieldRow = number of field rows, required if genLayout is TRUE
# serpentine = logical; if TRUE, plot numbers will be in serpentine arrangement, required if genLayout is TRUE
# outputFile = prefix to be used for the names of the output files
# outputPath = path where output will be saved
# ---------------------------------------------------------

suppressWarnings(suppressPackageStartupMessages(library(optparse)))
suppressWarnings(suppressPackageStartupMessages(library(PBTools)))

optionList <- list(
  make_option(opt_str = c("-n","--nTreatment"), type = "integer", default = NULL,
              help = "Number of entries", metavar = "number of entries"),
  make_option(opt_str = c("--nRowBlk"), type = "integer", default = NULL,
              help = "Number of row block per replicate", metavar = "number of row block per replicate"),
  make_option(opt_str = c("-r","--nRep"), type = "integer", default = NULL,
              help = "Number of replicates", metavar = "number of replicates"),
  make_option(opt_str = c("-t","--nTrial"), default = as.integer(1),
              help = "Number of trials", metavar = "number of trials"),
  make_option(opt_str = c("--genLayout"), type = "logical", default = F,
              help = "Whether layout will be generated or not", metavar = "whether layout will be generated or not"),
  make_option(opt_str = c("--nFieldRow"), type = "integer", default = as.integer(1),
              help = "Number of field rows", metavar = "number of field rows"),
  make_option(opt_str = c("--serpentine"), type = "logical", default = F,
              help = "Whether plot numbers will be in serpentine arrangement or not", 
              metavar = "Whether plot numbers will be in serpentine arrangement or not"),
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
  temp <- try(result <- designRowColumn(generate = list(Entry = opt$nTreatment),
                                        numRowBlk = opt$nRowBlk,
                                        numRep = opt$nRep,
                                        numTrial = opt$nTrial,
                                        genLayout = opt$genLayout,
                                        numFieldRow = opt$nFieldRow,
                                        serpentine = opt$serpentine,
                                        display = TRUE),
              silent = TRUE)
} else {
  temp <- try(result <- designRowColumn(generate = list(Entry = opt$nTreatment),
                                        numRowBlk = opt$nRowBlk,
                                        numRep = opt$nRep,
                                        numTrial = opt$nTrial,
                                        genLayout = opt$genLayout,
                                        display = TRUE),
              silent = TRUE)
}

if(all(class(temp) == "try-error")) {
  msg <- trimws(strsplit(temp, ":")[[1]])
  msg <- trimws(paste(strsplit(msg, "\n")[[length(msg)]], collapse = " "))
  cat("Error in designRowColumn:", msg, sep = "")
}

sink()

if(all(class(temp) == "try-error")) { stop(paste("Error in designRowColumn:", msg, sep = "")) }

# save the fieldbook to a csv file
write.csv(result$fieldbook, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_fieldbook.csv", sep = ""), row.names = FALSE)

if (opt$genLayout) {
  for (i in (1:length(result$plan$TrmtLayout))) {
    write.csv(result$plan$TrmtLayout[[i]], file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_", 
                                                        names(result$plan)[1],"_", names(result$plan$TrmtLayout)[i], ".csv", sep = ""))
  }
  
  for (i in 2:length(result$plan)) {
    write.csv(result$plan[[i]], file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_", names(result$plan)[i],".csv", sep = ""))
  }
} else {
  for (i in (1:length(unique(result$plan$TrmtLayout[,1])))) {
    tempTL <- result$plan$TrmtLayout[result$plan$TrmtLayout[,1] == unique(result$plan$TrmtLayout[,1])[i],]
    write.csv(tempTL, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_StatisticalDesignArray_", names(result$plan$TrmtLayout)[1], i, ".csv", sep = ""), row.names = FALSE)
    if (i == 1) {
      tempRBL <- result$plan$RowBlockLayout[result$plan$RowBlockLayout[,1] == unique(result$plan$RowBlockLayout[,1])[i],]
      tempRBL <- tempRBL[,2:ncol(tempRBL)]
      write.csv(tempRBL, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_", names(result$plan)[2],".csv", sep = ""), row.names = FALSE)
      
      tempCBL <- result$plan$ColumnBlockLayout[result$plan$ColumnBlockLayout[,1] == unique(result$plan$ColumnBlockLayout[,1])[i],]
      tempCBL <- tempCBL[,2:ncol(tempCBL)]
      write.csv(tempCBL, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_", names(result$plan)[3],".csv", sep = ""), row.names = FALSE)
      
    }
  }
}

