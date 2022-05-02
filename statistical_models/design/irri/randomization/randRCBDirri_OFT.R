# -------------------------------------------------------------------------------------
# Name             : randRCBDirri_OFT
# Description      : Generate randomization for On-Farm Trial using RCBD which can be  
#                    run in the command line with arguments
# R Version        : 4.1.1 
# Note             : with entryList as argument and uses entry_id in the randomization
# -------------------------------------------------------------------------------------
# Author           : Alaine A. Gulles 
# Author Email     : a.gulles@irri.org
# Date             : 2022.04.26
# Date Modified    : 2022.04.26
# Maintainer       : Alaine A. Gulles 
# Maintainer Email : a.gulles@irri.org
# Script Version   : 1
# Command          : Rscript randRCBDirri_OFT.R --entryList "RCBD_SD_0001.lst" 
#                    --nTrial 3 -o "Output" -p "D:/Results"  
# -------------------------------------------------------------------------------------
# Parameters:
# entryList = a cvs file containing the entry information
# nTrial = number of farm (occurrence)
# outputFile = prefix to be used for the names of the output files
# outputPath = path where output will be saved
# ---------------------------------------------------------

# load the needed packages
suppressWarnings(suppressPackageStartupMessages(library(optparse)))
suppressWarnings(suppressPackageStartupMessages(library(PBToolsDesign)))

optionList <- list(
  make_option(opt_str = c("--entryList"), type = "character", 
              help = "Entry List", metavar = "entry list"),
  make_option(opt_str = c("-t","--nTrial"), default = as.integer(1),
              help = "Number of farms", metavar = "number of farms"),
  make_option(opt_str = c("-o", "--outputFile"), type = "character", default = "RCBD_OFT_Expt",
              help = "Prefix to be used for the names of the output files",
              metavar = "prefix to be used for the names of the output files"),
  make_option(opt_str = c("-p", "--outputPath"), type = "character", default = getwd(),
              help = "Path where output will be saved",
              metavar = "path where output will be saved")
)

# garbage collection 
tmpGC <- gc()

# create an instance of a parser object
opt_parser = OptionParser(option_list = optionList)
opt = parse_args(opt_parser)

# check if folder is exist or not
if (!dir.exists(opt$outputPath)) {
  dir.create(opt$outputPath)
}

prevDir <- getwd()
setwd(opt$outputPath)

# read the file containing the entry list
entryData <- read.csv(file = opt$entryList)
entryInfo <- entryData[,"entry_id"]

# write the design information in a pdf
sink(file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_designInfo.txt", sep = ""))
temp <- try(result <- designRCBD(generate = list(Entry = entryInfo),
                                 numBlk = opt$nTrial,
                                 display = T), 
        
            silent = TRUE)  

if(all(class(temp) == "try-error")) {
  msg <- trimws(strsplit(temp, ":")[[1]])
  msg <- trimws(paste(strsplit(msg, "\n")[[length(msg)]], collapse = " "))
  cat("Error in designRCBD:", msg, sep = "")
}

sink()

if(all(class(temp) == "try-error")) { stop(paste("Error in designRCBD:", msg, sep = "")) }

# rename columns
fbook <- result[[1]]
names(fbook) <- c("occurrence", "replicate", "entry_id","plot_number")
fbook$occurrence <- fbook$replicate
fbook$plot_number <- rep(1:nrow(entryData), times = opt$nTrial)

# rearrange columns

nfbook <- fbook[, c("occurrence", "plot_number", "replicate", "entry_id")]

# save the design to a csv file
write.csv(nfbook, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_DesignArray.csv", sep = ""), row.names = FALSE)
