# -------------------------------------------------------------------------------------
# Name             : randPREPirri
# Description      : Generate randomization and layout for partially replicated (P-Rep) 
#                    Design which can be run in the command line with arguments and 
#                    accepts entry list
# R Version        : 4.0.3 
# Note             : with entryList as argument and uses entry_id in the randomization
# -------------------------------------------------------------------------------------
# Author           : Alaine A. Gulles 
# Author Email     : a.gulles@irri.org
# Date             : 2021.01.10
# Date Modified    : 2021.04.20
# Maintainer       : Alaine A. Gulles 
# Maintainer Email : a.gulles@irri.org
# Script Version   : 2
# Command          : Rscript randPREPirri.R --entryList "PREP_SD_0001.lst"
#                    --nTrial 3 --genLayout T --nFieldRow 8 --fieldOrder "CO" --serpentine T
#                    --topToBottom T -o "Output" -p "D:/Results"
# Remark           : remove the serpentine and topToBottom as argument for this script
#                    replace with fieldOrder
# -------------------------------------------------------------------------------------
# Parameters:
# entryList = a cvs file containing the entry information with entry type and number of replicates
# nTrial = number of trials (occurrence)
# genLayout = logical; if TRUE, layout will be generated
# nFieldRow = number of field rows, required if genLayout is TRUE
# fieldOrder = character with possible values" 'CO' (default), 'CS', 'RO','RS'
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
              help = "Number of trials", metavar = "number of trials"),
  make_option(opt_str = c("--genLayout"), type = "logical", default = F,
              help = "Whether layout will be generated or not", metavar = "whether layout will be generated or not"),
  make_option(opt_str = c("--nFieldRow"), type = "integer", default = as.integer(1),
              help = "Number of field rows", metavar = "number of field rows"),
  make_option(opt_str = c("--serpentine"), type = "character", default = "CO",
              help = "Indicates whether plot numbers will be in serpentine arrangement or not written from top-to-bottom or left-to-right", metavar = "Whether plot numbers will be in serpentine arrangement or not"),
  # make_option(opt_str = c("--serpentine"), type = "logical", default = F,
  #             help = "Whether plot numbers will be in serpentine arrangement or not", metavar = "Whether plot numbers will be in serpentine arrangement or not"),
  # make_option(opt_str = c("--topToBottom"), type = "logical", default = T,
  #             help = "Whether plot numbers will written top-to-bottom or left-to-right", metavar = "Whether plot numbers will written top-to-bottom or left-to-right"),
  make_option(opt_str = c("-o", "--outputFile"), type = "character", default = "PRep_Expt",
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

# read fieldOrder
fieldOrder <- opt$serpentine
serpentine <- F
topToBottom <- T

switch(fieldOrder, CO = {serpentine <<- F; topToBottom <<- T},
       CS = {serpentine <<- T; topToBottom <<- T},
       RO = {serpentine <<- F; topToBottom <<- F},
       RS = {serpentine <<- T; topToBottom <<- F})

# read the file containing the entry list
entryData <- read.csv(file = opt$entryList)
entryInfo <- entryData %>% arrange(desc(entry_type), nRep) %>% 
  dplyr::select(entry_id, entry_number, entry_name, entry_type)

# determine the rep grp per entrytype
entrySInfo1 <- entryData %>% group_by(entry_type, nRep) %>% 
  count(entry_type) %>% arrange(desc(entry_type))

# determine if check or test entry
entrySInfo2 <- entryData %>% group_by(entry_type) %>% count(entry_type) %>% arrange(desc(entry_type))

# write the design information
sink(file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_designInfo.txt", sep = ""))
if (opt$genLayout) {
  temp <- try(result <- designPrep(numRepPerTrmtGrp = entrySInfo1$nRep,
                                   numTrmtPerTrmtGrp = entrySInfo1$n,
                                   numTrmtPerGrp = entrySInfo2$n, 
                                   numTrial = opt$nTrial,
                                   genLayout = opt$genLayout,
                                   numFieldRow = opt$nFieldRow,
                                   treatName = entryInfo[,"entry_id"], 
                                   listName = "Entry",
                                   serpentine = serpentine,
                                   topToBottom = topToBottom,
                                   display = TRUE),
              silent = TRUE)
} else {
  temp <- try(result <- designPrep(numRepPerTrmtGrp = entrySInfo1$nRep,
                                   numTrmtPerTrmtGrp = entrySInfo1$n,
                                   numTrmtPerGrp = entrySInfo2$n, 
                                   numTrial = opt$nTrial,
                                   genLayout = opt$genLayout, 
                                   listName = "Entry", 
                                   treatName = entryInfo[,"entry_id"],
                                   display = T),
              silent = TRUE)
}

if(all(class(temp) == "try-error")) {
  msg <- trimws(strsplit(temp, ":")[[1]])
  msg <- trimws(paste(strsplit(msg, "\n")[[length(msg)]], collapse = " "))
  cat("Error in designPrep:", msg, sep = "")
}

sink()

if(all(class(temp) == "try-error")) { stop(paste("Error in designPrep:", msg, sep = "")) }

# rearrange columns and rename columns
fbook <- result[[1]]
# newData <- merge(fbook, entryInfo, 
#                  by.x = c("Entry","EntryType"), 
#                  by.y = c("entry_id","entry_type"))

newData <- merge(fbook, entryInfo, 
                 by.x = c("Entry"), 
                 by.y = c("entry_id"))

if (opt$genLayout) { 
  fbook <- newData %>% 
    relocate(Entry, entry_type, entry_name, .after = Rep) %>% 
    # dplyr::select(Trial, PlotNumber, Rep, Entry, entry_name, entry_type, 
    #               FieldRow, FieldColumn) %>% 
    dplyr::select(Trial, PlotNumber, Rep, Entry, entry_type, 
                  FieldRow, FieldColumn) %>% 
    arrange(Trial, FieldColumn, FieldRow) %>% 
    rename("occurrence" = "Trial", "replicate" = "Rep", "entry_id" = "Entry", 
           "plot_number" = "PlotNumber", "field_row" = "FieldRow", "field_col" = "FieldColumn")
  
} else { 
  fbook <- newData %>% 
    relocate(Entry, entry_type, entry_name, .after = Rep) %>% 
    # dplyr::select(Trial, PlotNumber, Rep, Entry, entry_name, entry_type) %>% 
    dplyr::select(Trial, PlotNumber, Rep, Entry, entry_type) %>% 
    arrange(Trial, PlotNumber) %>% 
    rename("occurrence" = "Trial", "replicate" = "Rep", "entry_id" = "Entry", 
           "plot_number" = "PlotNumber")
}

# save the fieldbook to a csv file
write.csv(fbook, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_DesignArray.csv", sep = ""), row.names = FALSE)

