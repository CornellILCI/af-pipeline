# -------------------------------------------------------------------------------------
# Name             : runALPHALATTICE
# Description      : Generate randomization and layout for Alpha Lattice Design which 
#                    can be run in the command line with arguments and accepts entry list
# R Version        : 3.5.1 
# Note             : with entryList as argument and uses entry_id in the randomization
# -------------------------------------------------------------------------------------
# Author           : Alaine A. Gulles 
# Author Email     : a.gulles@irri.org
# Date             : 2020.06.17
# Maintainer       : Alaine A. Gulles 
# Maintainer Email : a.gulles@irri.org
# Script Version   : 2
# Command          : Rscript runALPHALATTICE.R --entryList "D:SampleEntryList1_n24.csv"
#                    --nTrial 3 --nRep 4 --nBlk 4 --genLayout T --nRowPerBlk 2 
#                    --nRowPerRep 4 --nFieldRow 8 --serpentine F -o "Output1" 
#                    -p "D:/Results"
# -------------------------------------------------------------------------------------
# Parameters:
# entryList = a cvs file containing the entry information
# nTrial = number of trials (occurrence)
# nRep = number of replicates
# nBlk = number of blocks per replicate
# genLayout = logical; if TRUE, layout will be generated
# nFieldRow = number of field rows, required if genLayout is TRUE
# nRowPerRep = number of rows per replicate, required if genLayout is TRUE
# nRowPerBlk = number of rows per block, required if genLayout is TRUE
# serpentine = logical; if TRUE, plot numbers will be in serpentine arrangement, required if genLayout is TRUE
# outputFile = prefix to be used for the names of the output files
# outputPath = path where output will be saved
# ---------------------------------------------------------

# load the needed packages
suppressWarnings(suppressPackageStartupMessages(library(optparse)))
suppressWarnings(suppressPackageStartupMessages(library(PBTools)))

optionList <- list(
  make_option(opt_str = c("--entryList"), type = "character", 
              help = "Entry List", metavar = "entry list"),
  make_option(opt_str = c("-t","--nTrial"), default = as.integer(1),
              help = "Number of trials", metavar = "number of trials"),
  make_option(opt_str = c("-r","--nRep"), type = "integer", default = NULL,
              help = "Number of replicates", metavar = "number of replicates"),
  make_option(opt_str = c("-b","--nBlk"), type = "integer", default = NULL,
              help = "Number of blocks", metavar = "number of blocks"),
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

# garbage collection 
gc()

# create an instance of a parser object
opt_parser = OptionParser(option_list = optionList)
opt = parse_args(opt_parser)

# check if folder is exist or not
if (!dir.exists(opt$outputPath)) {
  dir.create(opt$outputPath)
}

# read the file containing the entry list
entryData <- read.csv(file = opt$entryList)
entryInfo <- entryData[,"entry_id"]

# write the design information
sink(file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_designInfo.txt", sep = ""))
if (opt$genLayout) {
  temp <- try(result <- designAlphaLattice(generate = list(Entry = entryInfo),
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
  temp <- try(result <- designAlphaLattice(generate = list(Entry = entryInfo),
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

# rename columns
fbook <- result[[1]]
if (opt$genLayout) { names(fbook) <- c("occurrence", "replicate", "block","entry_id","plot_number", "field_row", "field_col")  
} else { names(fbook) <- c("occurrence", "replicate", "block","entry_id","plot_number") }


# rearrange columns
if (opt$genLayout) { nfbook <- fbook[,c("occurrence", "plot_number", "replicate", "block", "entry_id","field_row", "field_col")]
} else { nfbook <- fbook[,c("occurrence", "plot_number", "replicate", "block", "entry_id")] }

# save the fieldbook to a csv file
write.csv(nfbook, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_DesignArray.csv", sep = ""), row.names = FALSE)
