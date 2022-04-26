# -------------------------------------------------------------------------------------
# Name             : randIBD_OFT
# Description      : Generate randomization and layout for Incomplete Block Design to be used in On-Farm Trials
# R Version        : 4.1.3
# -------------------------------------------------------------------------------------
# Author           : Pedro A M Barbosa
# Author Email     : p.medeiros@cgiar.org
# Date             : 2022.Apr.15
# Maintainer       : Pedro A M Barbosa 
# Maintainer Email : p.medeiros@cgiar.org
# Script Version   : 1
# Syntax           : "Rscript randIBD_OFT.R -e randIBD_OFT_SD_0001.lst --sBlk 3 --nTrial 100"
# -------------------------------------------------------------------------------------
# Parameters:
# entryList = csv file that contains the entry list
# nTrial = number of Occurrences/Farms
# sBlk = number of plot in each block (block = farm)
# outputFile = prefix to be used for the names of the output files
# outputPath = path where output will be saved
# ---------------------------------------------------------


# load the needed packages
suppressWarnings(suppressPackageStartupMessages(library(optparse)))
suppressWarnings(suppressPackageStartupMessages(library(ebsRtools)))

optionList <- list(
  make_option(opt_str = c("-e","--entryList"), type = "character", default = "randIBD_OFT_SD_0001.lst",
              help = "name of the csv file with the entry list", metavar = "entry list"),
  make_option(opt_str = c("-k","--sBlk"), type = "integer", default = 3,
              help = "Number of plots in each block", metavar = "size of blocks"),
  make_option(opt_str = c("-t","--nTrial"),  type = "integer", default = as.integer(100),
              help = "Number of occurrences", metavar = "number of occurrences"),
  make_option(opt_str = c("-o", "--outputFile"), type = "character", default = "IBD_OFT_Expt_",
              help = "Prefix to be used for the names of the output files",
              metavar = "prefix to be used for the names of the output files"),
  make_option(opt_str = c("-p", "--outputPath"), type = "character", default = getwd(),
              help = "Path where output will be saved", metavar = "path where output will be saved")
)

# create an instance of a parser object
opt_parser = OptionParser(option_list = optionList)
opt = parse_args(opt_parser)

# check if folder does exist or not
if (!dir.exists(opt$outputPath)) {
  dir.create(opt$outputPath)
}

# Reading the entry list
entryList <- read.csv(opt$entryList, h = T)
nTreatment <- nrow(entryList)

nCheck <- sum(entryList$entry_type=="check")
if(nCheck<3){stop("Error in randIBD_OFT: The entry list should contain at least 3 checks")}

nTest <- sum(entryList$entry_type=="test")
if(nTest<3){stop("Error in randIBD_OFT: The experiment should evaluate at least 3 new genotypes (test entriess)")}

if(opt$sBlk<3){stop("Error in randIBD_OFT: The block size should be bigger than 2")}
if(length(unique(entryList$entry_id))!=nTreatment){stop("Error in randIBD_OFT: There are more than one entry with the same id.")}

checks <- entryList$entry_id[entryList$entry_type=="check"]
test <- entryList$entry_id[entryList$entry_type=="test"]

if(opt$sBlk > nCheck | opt$sBlk > nTest){stop("Error in randIBD_OFT: Block size should be smaller than the number of checks and test entries")}

if(!(nCheck + nTest == nTreatment)) {stop("Error in randIBD_OFT: Please, Entry types should be 'test' or 'check')")}
if(nCheck== 0) {stop("Error in randIBD_OFT: Check entries not found, check genotypes are required for this design)")}

# Creating the 4 types of experiments

## Exp1 All entries
exp1 <- combn(entryList$entry_id,opt$sBlk)

## Exp2 Only test
exp2 <- combn(test,opt$sBlk)

## Exp3 Each check with each pair of test
test1 <- combn(checks,opt$sBlk-1)
exp3 <- matrix(NA,opt$sBlk,nTest*ncol(test1))
exp3[c(1:(opt$sBlk-1)),] <- test1
exp3[opt$sBlk,] <- rep(test,each=ncol(test1))

## Exp4 Each test with each pair of check
test2 <- combn(test,opt$sBlk-1)
exp4 <- matrix(NA,opt$sBlk,nCheck*ncol(test2))
exp4[c(1:(opt$sBlk-1)),] <- test2
exp4[opt$sBlk,] <- rep(checks,each=ncol(test2))

exps <- list(exp1,exp2,exp3,exp4)
n1 <- ncol(exp1)
n2 <- ncol(exp2)
n3 <- ncol(exp3)
n4 <- ncol(exp4)
nu <- c(n1,n2,n3,n4)
names(exps) <- nu

# Creating all comninations of the experiments that result nTrial
combSum <- function(s, x, xhead = head(x,1), r = c()) {
  if (s == 0) {
    return(list(r))
  } else {
    x <- sort(x,decreasing = T)
    return(unlist(lapply(x[x<=min(xhead,s)], function(k) combSum(round(s-k,10), x[x<= round(s-k,10)], min(k,head(x[x<=round(s-k,10)],1)), c(r,k))),recursive = F)) 
  }
}

wholeExp <- combSum(opt$nTrial,c(nu))

if(is.null(wholeExp)){stop("Error in randIBD_OFT: No combinations were found for this entry list, block size and number of farms. Try to update one of these inputs")}

# Eliminating design options based on some QC rules
qc <- matrix(NA,length(wholeExp),4)
for(i in 1:length(wholeExp)){
  qc[i,1] <- length(unique(wholeExp[[i]]))>2 # eliminate those combinations with only 1 or 2 types of experiment
  qc[i,2] <- n2 %in% wholeExp[[i]] # eliminate those combinations that do not contain the exp2
  #qc[i,3] <- length(unique(wholeExp[[i]]))==4 # eliminate those combinations that do not contain all 4 experiment types
  qc[i,4] <- all(qc[i,],na.rm=T)
}
wholeExp <- wholeExp[qc[,4]]

if(length(wholeExp)==0){stop("Error in randIBD_OFT: No combination met the quality control parameters")}

# Selecting one of the the available combinations

selectedExp <- wholeExp[[1]] # pick the 8 while no method for this selection is implemented

## generating whole experiment based on the selected combination
for(i in 1:length(table(selectedExp))){
  if(i==1){
    tmp <- do.call("cbind", replicate(table(selectedExp)[i], exps[[names(table(selectedExp))[i]]], simplify = FALSE))
  }else{
    tmp <- cbind(tmp,do.call("cbind", replicate(table(selectedExp)[i], exps[[names(table(selectedExp))[i]]], simplify = FALSE)))
  }
}

DesignArray <- data.frame(occurrence=rep(1:opt$nTrial,each=opt$sBlk),
                          plot_num = rep(1:3,opt$nTrial),
                          block=rep(1:opt$nTrial,each=opt$sBlk),
                          entry_id = unlist(as.data.frame(tmp)))

# save the Design Array to a csv file
write.csv(DesignArray, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_DesignArray.csv", sep = ""), row.names = FALSE)