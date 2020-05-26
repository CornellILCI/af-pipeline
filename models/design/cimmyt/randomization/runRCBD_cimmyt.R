# -------------------------------------------------------------------------------------
# Name             : runRCBD 
# Description      : Generate randomization and layout for RCBD which can be run in the 
#                    command line with arguments
# R Version        : 3.6.1 
# -------------------------------------------------------------------------------------
# Author           : Pedro A M Barbosa | Alaine A. Gulles | Rose Imee Zhella A. Morantte
# Author Email     : p.medeiros@cgiar.org
# Date             : 2020.Mar.5
# Maintainer       : Pedro A M Barbosa 
# Maintainer Email : p.medeiros@cgiar.org
# Script Version   : 2
# Syntax example   : "Rscript runRCBD_cimmyt.R -n 25 -b 3 -t 3 --nFieldRow 5 --nPlotBarrier 5"
# -------------------------------------------------------------------------------------
# Parameters:
# nTreatment = number of entries
# nRep = number of replicates (replicate_block)
# nTrial = number of Occurrences
# genLayout = logical; if TRUE, layout will be generated
# nFieldRow = number of field rows, required if genLayout is TRUE
# nPlotBarrier = number of plots up to the barrier
# randFirst = if thefirst rep should be randomized
# Vserpentine = logical; if TRUE, plot numbers will be in vertical serpentine arrangement, required if genLayout is TRUE
# outputFile = prefix to be used for the names of the output files
# outputPath = path where output will be saved
# ---------------------------------------------------------


# load the needed packages
suppressWarnings(suppressPackageStartupMessages(library(optparse)))
suppressWarnings(suppressPackageStartupMessages(library(ebsRtools)))

optionList <- list(
  make_option(opt_str = c("-n","--nTreatment"), type = "integer", default = NULL,
              help = "Number of entries", metavar = "number of entries"),
  make_option(opt_str = c("-b","--nRep"), type = "integer", default = NULL,
              help = "Number of blocks or replicates", metavar = "number of blocks or replicates"),
  make_option(opt_str = c("-t","--nTrial"), default = as.integer(3),
              help = "Number of occurrences", metavar = "number of occurrences"),
  make_option(opt_str = c("--genLayout"), type = "logical", default = T,
              help = "Whether layout will be generated or not", metavar = "whether layout will be generated or not"),
  make_option(opt_str = c("--nFieldRow"), type = "integer", default = NULL,
              help = "Number of field rows", metavar = "number of field rows"),
  make_option(opt_str = c("--nPlotBarrier"), type = "integer", default = NULL,
              help = "Number of plots up to the barrier, if is in Vserpentine it is in vertical direction", metavar = "number of plots up to barrier"),
  make_option(opt_str = c("--Vserpentine"), type = "logical", default = F,
              help = "Whether plot numbers will be in Vertical serpentine arrangement or Horizontal", metavar = "Vertical or Horizontal serpentine"),
  make_option(opt_str = c("-f","--rand1"), type = "logical", default = T,
              help = "If the entries should be randomized in the first rep", metavar = "randomize first rep"),
  make_option(opt_str = c("-o", "--outputFile"), type = "character", default = "RCBD_Expt_",
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

entry <- c(1:opt$nTreatment)
trialsName <- paste("Occurrence",c(1:opt$nTrial), sep="_")
trials <- list()

tag <-  floor(log10(opt$nTreatment))+1

# randomization and write the design information in a txt file
sink(file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_DesignInfo.txt", sep = ""))
temp <- try(
  for(i in 1:opt$nTrial){
    trial <- randRCBD(trt = entry,
                         r = opt$nRep,
                         tag = tag)
    trials[[i]] <- trial
  }
)
names(trials) <- trialsName

if(all(class(temp) == "try-error")) {
  msg <- trimws(strsplit(temp, ":")[[1]])
  msg <- trimws(paste(strsplit(msg, "\n")[[length(msg)]], collapse = " "))
  cat("Error in randRCBD:", msg, sep = "")
} else {
  msg <- trials[[1]]$parameters
  cat("Design:",toupper(msg$design),"\n")
  cat("Number of Genotypes:",length(msg$trt),"\n")
  cat("Number of Occurrences:",opt$nTrial,"\n")
  cat("Number of Blocks (Replicates) per occurrence:",msg$r,"\n")
  #cat("Number of Field Rows:",opt$nFieldRow)
      }
sink()

if(all(class(temp) == "try-error")) { stop(paste("Error in randRCBD:", msg, sep = "")) }

if(opt$genLayout){
  trials <- add.layout(trials = trials,
                       Vserpentine = opt$Vserpentine,
                       nFieldRow = opt$nFieldRow,
                       nPlotsRepBarrier = opt$nPlotBarrier,
                       save = TRUE,
                       outputPath = opt$outputPath,
                       outputFile = opt$outputFile)
}

for(i in c(1:length(trials))){
  occurrence <- rep(i,length=length(trials[[i]]$book$plots))
  trials[[i]]$book <- cbind(occurrence,trials[[i]]$book)
}

DesingArray <- trials[[1]]$book
if(opt$nTrial>1){
  for(i in 2:opt$nTrial){
    DesingArray <- rbind(DesingArray,trials[[i]]$book)
  }
}

# save the Design Array to a csv file
write.csv(DesingArray, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_DesignArray.csv", sep = ""), row.names = FALSE)
