# -------------------------------------------------------------------------------------
# Name             : runALPHA_wheat
# Description      : Generate randomization and layout for Alpha-Lattice which can be run in the 
#                    command line with arguments
# R Version        : 3.6.1 
# -------------------------------------------------------------------------------------
# Author           : Pedro A M Barbosa | Alaine A. Gulles | Rose Imee Zhella A. Morantte
# Author Email     : p.medeiros@cgiar.org
# Date             : 2020.Mar.12
# Maintainer       : Pedro A M Barbosa 
# Maintainer Email : p.medeiros@cgiar.org
# Script Version   : 2
# Syntax example  : "Rscript runALPHA_cimmyt_wheat.R -n 45 -b 3 -k 5 -t 3 --RandOcc FALSE --rand1 FALSE --nFieldRow 9 --nPlotBarrier 5"
# -------------------------------------------------------------------------------------
# Parameters:
# nTreatment = number of entries
# nRep = number of replicates (replicate_block)
# nTrial = number of Occurrences
# sBlk = number of plot in each block (block size)
# rand1 = logical; if TRUE, the first rep will be randomized
# RandOcc = logical; if TRUE, run a different randomization for each occurrrence
# genLayout = logical; if TRUE, layout will be generated
# nFieldRow = number of field rows, required if genLayout is TRUE
# Vserpentine = logical; if TRUE, plot numbers will be in Vertical serpentine arrangement, required if genLayout is TRUE
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
              help = "Number of replicates or super-blocks", metavar = "number replicates or super-blocks"),
  make_option(opt_str = c("-k","--sBlk"), type = "integer", default = NULL,
              help = "Number of plots in each block", metavar = "size of blocks"),
  make_option(opt_str = c("--rand1"), type = "logical", default = T,
              help = "Randomize the first rep", metavar = "rep 1 randomization"),
  make_option(opt_str = c("--RandOcc"), type = "logical", default = T,
              help = "Run a new randomization for each occurrence", metavar = "Same randomizationin all occurrences"),
  make_option(opt_str = c("-t","--nTrial"),  type = "integer", default = as.integer(1),
              help = "Number of occurrences", metavar = "number of occurrences"),
  make_option(opt_str = c("--genLayout"), type = "logical", default = T,
              help = "Whether layout will be generated or not",
              metavar = "whether layout will be generated or not"),
  make_option(opt_str = c("--nFieldRow"), type = "integer", default = as.integer(1),
              help = "Number of field rows",  metavar = "number of field rows"),
  make_option(opt_str = c("--nPlotBarrier"), type = "integer", default = NULL,
              help = "Number of plots up to the barrier, if is in Vserpentine it is in vertical direction", metavar = "number of plots up to barrier"),
  make_option(opt_str = c("--Vserpentine"), type = "logical", default = F,
              help = "Whether plot numbers will be in Vertical serpentine arrangement or Horizontal",
              metavar = "Vertical or Horizontal serpentine"),
  make_option(opt_str = c("-o", "--outputFile"), type = "character", default = "AL_Expt_wheat_",
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

if(opt$nTreatment%%opt$sBlk != 0) {stop("Error in randAPLHA: The size of the block is not appropriate, the number of treatments must be multiple of k (block size)")}
#if(opt$nRep <2 | opt$nRep >4) {stop("Error in randAPLHA: The number or replicates should be 2, 3 or 4")} #This is if use agricolae

entry <- c(1:opt$nTreatment)
trialsName <- paste("Occurrence",c(1:opt$nTrial), sep="")
trials <- list()

tag <-  floor(log10(opt$nTreatment))+1

# randomization and write the design information in a txt file
sink(file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_DesignInfo.txt", sep = ""))
temp <- try(trials <- randALPHA(trt = entry,
                                 k = opt$sBlk,
                                 r = opt$nRep,
                                 tag = tag,
                                 nTrial = ifelse(!opt$RandOcc,1,opt$nTrial)),
            silent = T)

if(all(class(temp) == "try-error" | !is.list(temp))) {
  msg <- trimws(strsplit(temp, ":")[[1]])
  msg <- trimws(paste(strsplit(msg, "\n")[[length(msg)]], collapse = " "))
  cat("Error in randALPHA: ", msg, sep = "")
} else{
  if(!opt$RandOcc & opt$nTrial>1){
    for(i in (2:opt$nTrial)){
      trials[[i]] <- trials[[1]]
    }
  }
  msg <- trials[[1]]$parameters
  for(i in (1:opt$nTrial)){
    cat("\nOccurrence",i,"\n")
    cat("Design:",toupper(trials[[i]]$parameters$design),"\n")
    cat("Concurrences:",trials[[i]]$parameters$Concurrences,"\n")
    if(trials[[i]]$parameters$design == "Alpha-Lattice"){
      cat("The design may not be an Alpha-Lattice (0,1)\n")
      if(opt$sBlk > (opt$nTreatment/opt$sBlk)){
        cat("It is preferable to use several small blocks rather than a few large blocks\n",
            "Consider to use",opt$sBlk,"blocks","with size of",opt$nTreatment/opt$sBlk,"plots each\n",
            "and check the conditions for the existence of an Alpha(0,1)-design\n")}
    }
  }
  cat("\nEXPERIMENT PARAMETERS:\n")
  cat("Number of Genotypes:",length(msg$trt),"\n")
  cat("Number of Occurrences:",opt$nTrial,"\n")
  cat("Number of Replicates (super-block) per Trial:",msg$r,"\n")
  cat("Number of Plots per block (Block Size):",msg$k,"\n")
  cat("Number of Blocks per Rep:",length(msg$trt)/msg$k,"\n")
  cat("Efficiency:",round(msg$Efficiency,4))
  if(length(trials)>0)
    names(trials) <- trialsName
  }
sink()

if(all(class(temp) == "try-error")) { stop(paste("Error in randAPLHA:", msg, sep = "")) }

if(!opt$rand1){
  for(i in 1:opt$nTrial){
    wht <- data.frame(entry = trials[[i]]$book$entry[1:opt$nTreatment],trt = entry)
    wht$trt <- as.character(wht$trt)
    
    bookWht <- trials[[i]]$book[,c("plots","entry","block","rep")]
    bookWht <- merge(bookWht[,c("plots","entry","block","rep")],
                     wht[,c("trt","entry")])
    bookWht <- bookWht[with(bookWht,order(plots)),]
    bookWht <- bookWht[,c("plots","block","rep","trt")]
    colnames(bookWht)[colnames(bookWht)=="trt"] <- "entry"
    trials[[i]]$book <- bookWht
    rownames(trials[[i]]$book) <- c(1:nrow(trials[[i]]$book))
  }
}

if(is.null(opt$nPlotBarrier)){
  opt$nPlotBarrier <- opt$sBlk
}

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
write.csv(DesingArray, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_DesingArray.csv", sep = ""), row.names = FALSE)
