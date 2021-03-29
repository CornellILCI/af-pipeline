# -------------------------------------------------------------------------------------
# Name             : runSingleTrial
# Description      : Perform single environment analysis
# R Version        : 3.5.3 
# -------------------------------------------------------------------------------------
# Author           : Alaine A. Gulles 
# Author Email     : a.gulles@irri.org
# Date             : 2019.11.25
# Maintainer       : Alaine A. Gulles 
# Maintainer Email : a.gulles@irri.org
# Script Version   : 3 (final)
# -------------------------------------------------------------------------------------
# Parameters:
# sourcePath = source file
# data = a data frame containing the variables that will be used for the analysis
# pedData = a data frame containing the pedigree information
# trialName = name of the column for the study name
# designName = name of the column for the experimental design used
# trait = name of the column for the response variable
# treatmentName = name of the column for the designation or mgids
# replicateName = name of the column for the replication
# blockName = name of the column for the block
# rowBlockName = name of the column for the row block
# columnBlockName = name of the column for the column block
# fieldRowName = name of the column for the row coordinates
# fieldColumnName = name of the column for the column 
# outputPath = path where output will be saved
# ---------------------------------------------------------

suppressWarnings(suppressPackageStartupMessages(library(optparse)))
suppressWarnings(suppressPackageStartupMessages(library(PBToolsAnalysis)))

optionList <- list(
  make_option(opt_str = c("--sourcePath"), type = "character", 
              help = "Source file", metavar = "source file"),
  make_option(opt_str = c("--data"), type = "character", 
              help = "Phenotypic file", metavar = "phenotypic file"),
  make_option(opt_str = c("--pedData"), type = "character", default = NULL,
              help = "Pedigree file", metavar = "pedigree file"),
  make_option(opt_str = c("--trialName"), type = "character",
              help = "Study Name", metavar = "study name"),
  make_option(opt_str = c("--designName"), type = "character",
              help = "Experimental Design", metavar = "experimental design"),
  make_option(opt_str = c("--trait"), type = "character", 
              help = "Response Variable", metavar = "response variable"),
  make_option(opt_str = c("--treatmentName"), type = "character", 
              help = "Treatment", metavar = "Treatment"),
  make_option(opt_str = c("--replicateName"), type = "character",
              help = "replicate", metavar = "replicate"),
  make_option(opt_str = c("--blockName"), type = "character", default = NULL,
              help = "Block", metavar = "block"),
  make_option(opt_str = c("--rowBlockName"), type = "character", default = NULL,
              help = "Row Block", metavar = "row block"),
  make_option(opt_str = c("--columnBlockName"), type = "character", default = NULL,
              help = "Column Block", metavar = "column block"),
  make_option(opt_str = c("--fieldRowName"), type = "character", default = NULL,
              help = "Fieldrow", metavar = "fieldrow"),
  make_option(opt_str = c("--fieldColumnName"), type = "character", default = NULL,
              help = "Fieldcolumn", metavar = "fieldcolumn"),
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

# source file
# source(opt$sourcePath)

# read the dataset
mydata <- read.csv(file = opt$data)

if (is.null(opt$pedData)) {
  temp <- try(seaResult <- singleTrials(dat = mydata, ped = NULL,
                                        trialvar = opt$trialName,
                                        designvar = opt$designName,
                                        trait = opt$trait, lwrlim=0, uprlim=15000,
                                        idvar = opt$treatmentName, missingHillsvar = NULL,
                                        rep_var = opt$replicateName,
                                        colblk_var = opt$columnBlockName,
                                        rowblk_var = opt$rowBlockName,
                                        blk_var = opt$blockName,
                                        colcoord_var = opt$fieldColumnName,
                                        rowcoord_var = opt$fieldRowName,
                                        workspace='2gb', pworkspace='2gb', saveModobj = TRUE),
              silent = TRUE)
}

if(all(class(temp) == "try-error")) {
  msg <- trimws(strsplit(temp, ":")[[1]])
  msg <- trimws(paste(strsplit(msg, "\n")[[length(msg)]], collapse = " "))
  sink(file = paste0(opt$outputPath, "/errorMessages.txt"))
  cat("Error in asreml: ", msg, sep = "")
  sink()
  stop(paste("Error in asreml: ", msg, sep = "")) 
}

if (is.null(opt$pedData)) {
  estimates <- seaResult$results_all
  estimates$PredictedValue <- estimates$predicted.value + estimates$trial.mean
  estimatesOutput <- estimates[,c("study", "mgid", "PredictedValue", "std.error", "Reliability")]
  names(estimatesOutput) <- c(opt$trialName, opt$treatmentName, "PredictedValue", "StdError", "Reliability")
}

numTrial <- length(unique(estimatesOutput[,opt$trialName]))

for (i in 1:numTrial) {
  outputPerTrial <- estimatesOutput[which(estimatesOutput[,opt$trialName] == unique(estimatesOutput[,opt$trialName])[i]),]
  write.csv(outputPerTrial, file = paste0(opt$outputPath,"/", unique(estimatesOutput[,opt$trialName])[i], "_",opt$trait,"_Single Trial Results.csv"), row.names = FALSE)
}

