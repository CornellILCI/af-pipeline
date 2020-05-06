# -------------------------------------------------------------------------------------
# Name             : runRCBD 
# Description      : Generate randomization and layout for RCBD which can be run in the 
#                    command line with arguments
# R Version        : 3.5.1 
# -------------------------------------------------------------------------------------
# Author           : Alaine A. Gulles | Rose Imee Zhella A. Morantte
# Author Email     : a.gulles@irri.org | r.morantte@irri.org
# Date             : 2019.01.18
# Maintainer       : Alaine A. Gulles 
# Maintainer Email : a.gulles@irri.org
# Script Version   : 2
# -------------------------------------------------------------------------------------
# Parameters:
# nTreatment = number of entries
# nRep = number of replicates (replicate_block)
# nTrial = number of trials (location rep)
# genLayout = logical; if TRUE, layout will be generated
# nFieldRow = number of field rows, required if genLayout is TRUE
# nRowPerRep = number of rows per replicate, required if genLayout is TRUE
# serpentine = logical; if TRUE, plot numbers will be in serpentine arrangement, required if genLayout is TRUE
# outputFile = prefix to be used for the names of the output files
# outputPath = path where output will be saved
# ---------------------------------------------------------

 
# load the needed packages
suppressWarnings(suppressPackageStartupMessages(library(optparse)))
suppressWarnings(suppressPackageStartupMessages(library(PBTools)))

optionList <- list(
  make_option(opt_str = c("-n","--nTreatment"), type = "integer", default = NULL,
              help = "Number of entries", metavar = "number of entries"),
  make_option(opt_str = c("-b","--nRep"), type = "integer", default = NULL,
              help = "Number of blocks or replicates", metavar = "number of blocks or replicates"),
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

# write the design information in a pdf
sink(file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_designInfo.txt", sep = ""))
if (opt$genLayout) {
  temp <- try(result <- designRCBD(generate = list(Entry = opt$nTreatment),
                                   numBlk = opt$nRep,
                                   numTrial = opt$nTrial,
                                   genLayout = opt$genLayout,
                                   numFieldRow = opt$nFieldRow,
                                   numRowPerBlk = opt$nRowPerRep,
                                   serpentine = opt$serpentine,
                                   topToBottom = T,
                                   display = T), 
              silent = TRUE)
} else {
  temp <- try(result <- designRCBD(generate = list(Entry = opt$nTreatment),
                                   numBlk = opt$nRep,
                                   numTrial = opt$nTrial,
                                   genLayout = opt$genLayout,
                                   display = T), 
              silent = TRUE)  
}

if(all(class(temp) == "try-error")) {
  msg <- trimws(strsplit(temp, ":")[[1]])
  msg <- trimws(paste(strsplit(msg, "\n")[[length(msg)]], collapse = " "))
  cat("Error in designRCBD:", msg, sep = "")
}

sink()

if(all(class(temp) == "try-error")) { stop(paste("Error in designRCBD:", msg, sep = "")) }

# rename the Block column
fbook <- result[[1]]
names(fbook)[match("Block", names(fbook))] <- "Rep"

# save the fieldbook to a csv file
write.csv(fbook, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_fieldbook.csv", sep = ""), row.names = FALSE)

if (opt$genLayout) {
  names(result[[2]])[3] <- "RepLayout"
  for (i in (1:length(result[[2]][[1]]))) {
    temp <- result[[2]][[1]][[i]]
    write.csv(temp, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_TrmtLayout_",names(result[[2]][[1]])[i], ".csv", sep = ""))
  }
  
  for (i in 2:length(result[[2]])) {
    write.csv(result[[2]][[i]], file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_", names(result[[2]])[i],".csv", sep = ""))
  }
} else {
  for (i in (1:nlevels(result[[2]][,1]))) {
    tempDF <- result[[2]][result[[2]][,1] == levels(result[[2]][,1])[i],]  

    # rename the Block column
    names(tempDF)[2:ncol(tempDF)] <- paste("Rep", 1:opt$nRep, sep = "")
    
    write.csv(tempDF, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_StatisticalDesignArray_",names(result[[2]])[1], i, ".csv", sep = ""), row.names = FALSE)
  }
}

