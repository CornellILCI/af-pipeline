# -------------------------------------------------------------------------------------
# Name             : randAugUnrep
# Description      : Generate randomization and layout for P-rep CRD w/ diagonal systematic checks
# R Version        : 4.0.3 
# -------------------------------------------------------------------------------------
# Author           : Pedro A M Barbosa | Alaine A. Gulles | Rose Imee Zhella A. Morantte
# Author Email     : p.medeiros@cgiar.org
# Date             : 2021.Mar.20
# Maintainer       : Pedro A M Barbosa 
# Maintainer Email : p.medeiros@cgiar.org
# Script Version   : 1
# Syntax           : "Rscript randAugUnrep.R --entryList "AUGUNREP_cimmyt_SD_0001.lst" --nTrial 2 --pCheck 10 --nFieldCol 20"
# -------------------------------------------------------------------------------------
# Parameters:
# entryList = csv file that contains the entry list
# nTrial = number of Occurrences
# genLayout = logical; fixed as TRUE
# fillGap = if the gaps should receive entry values as "filler" or just removed
# nFieldRow = number of field rows, fixed in 999
# pCheck = percentage of check plots to be filled with check entries
# nFieldCol = number of field columns, required
# outputFile = prefix to be used for the names of the output files
# outputPath = path where output will be saved
# ---------------------------------------------------------


# load the needed packages
suppressWarnings(suppressPackageStartupMessages(library(optparse)))
suppressWarnings(suppressPackageStartupMessages(library(ebsRtools)))

optionList <- list(
  make_option(opt_str = c("-e","--entryList"), type = "character", default = NULL,
              help = "name of the csv file with the entry list", metavar = "entry list"),
  make_option(opt_str = c("-t","--nTrial"),  type = "integer", default = as.integer(1),
              help = "Number of occurrences", metavar = "number of occurrences"),
  make_option(opt_str = c("--pCheck"),  type = "numeric", default = 10,
              help = "Percentage of check plots in the field", metavar = "percentage of check plots"),
  make_option(opt_str = c("--genLayout"), type = "logical", default = T,
              help = "Whether layout will be generated or not",
              metavar = "whether layout will be generated or not"),
  make_option(opt_str = c("--fillGap"), type = "logical", default = F,
              help = "Whether fill the gap with filler or let them as empty plots",
              metavar = "whether layout will be generated or not"),
  make_option(opt_str = c("--nFieldRow"), type = "integer", default = as.integer(999),
              help = "Number of field rows",  metavar = "number of field rows"),
  make_option(opt_str = c("--nFieldCol"), type = "integer", default = as.integer(20),
              help = "Number of field columns",  metavar = "number of field columns"),
  make_option(opt_str = c("-o", "--outputFile"), type = "character", default = "AugUnrep_Expt_",
              help = "Prefix to be used for the names of the output files",
              metavar = "prefix to be used for the names of the output files"),
  make_option(opt_str = c("-p", "--outputPath"), type = "character", default = getwd(),
              help = "Path where output will be saved", metavar = "path where output will be saved")
)

## create an instance of a parser object
opt_parser = OptionParser(option_list = optionList)
opt = parse_args(opt_parser)

# check if folder does exist or not
if (!dir.exists(opt$outputPath)) {
  dir.create(opt$outputPath)
}

entryList <- read.csv(opt$entryList, h = T)
if(sum(entryList$entry_role=="repeated check")>1 & is.null(entryList$nRep)){
  stop("The Augmented Unrep design requires")
}

nNonSptCheck <- sum(entryList$entry_role!="spatial check")
nSptCheck <- sum(entryList$entry_role=="spatial check")
nTreatment <- nrow(entryList)

nonSptEntries_id <- entryList$entry_id[entryList$entry_role!="spatial check"]
sptCheck_id <- entryList$entry_id[entryList$entry_role=="spatial check"]

nReplicate <- entryList$nRep[entryList$entry_role!="spatial check"]

trialsName <- paste("Occurrence",c(1:opt$nTrial), sep="")
trials <- list()

tag <-  floor(log10(nTreatment))+1
entry <- nonSptEntries_id
# randomization and write the design information in a txt file
#sink(file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_DesignInfo.txt", sep = ""))
temp <- try(trials <- randCRAND(trt = entry,
                                r = nReplicate,
                                tag = tag,
                                nTrial = opt$nTrial),
            silent = T)

if(all(class(temp) == "try-error" | !is.list(temp))) {
  msg <- trimws(strsplit(temp, ":")[[1]])
  msg <- trimws(paste(strsplit(msg, "\n")[[length(msg)]], collapse = " "))
  cat("Error in randCRAND: ", msg, sep = "")
} else{
  msg <- trials[[1]]$parameters
  #for(i in (1:opt$nTrial)){
    #cat("\nOccurrence",i,"\n")
    #cat("Design: P-rep CRD w/ diagonal systematic checks","\n")
  #}
  #cat("\nEXPERIMENT PARAMETERS:\n")
  #cat("Number of Occurrences:",opt$nTrial,"\n")
  #cat("Number of no-spatial entries:",nNonSptCheck,"\n")
  #cat("Number of spatial Checks:",nSptCheck,"\n")
  #cat("Percentage of checks",opt$pCheck,"%","\n")
  if(length(trials)>0)
    names(trials) <- trialsName
}
#sink()

if(all(class(temp) == "try-error")) { stop(paste("Error in randCRAND:", msg, sep = "")) }

if(opt$genLayout){
  layout <- diagLayout(opt$nFieldCol,opt$nFieldRow,percentChk = opt$pCheck/100)
  
  number <- 10
  if (tag > 0){
    number <- 10^tag
  }
  fbook <- data.frame(plot_number = number + (1:(opt$nFieldRow*opt$nFieldCol)),
                      field_row = rep(c(1:opt$nFieldRow), each= opt$nFieldCol),
                      field_col = rep(c(1:opt$nFieldCol), opt$nFieldRow),
                      check = as.vector(t(layout)))
  
  fbook$entry <- NA
  for(i in 1:opt$nTrial){
    #add check entries randomly to the check plots
    tmp_fbook <- fbook
    tmp_fbook[tmp_fbook$check==1,"entry"] <- as.vector(replicate(sum(tmp_fbook$check)/nSptCheck,{
      sample(sptCheck_id)}))[1:sum(tmp_fbook$check)]
    #add test entries to the non-check plots, following the CRD randomization results 
    tmp_fbook[tmp_fbook$check==0,"entry"][1:length(trials[[i]]$book$entry)] <-  trials[[i]]$book$entry
    tmp_fbook$replicate <- 1
    tmp_fbook$occurrence <- i
    colnames(tmp_fbook)[colnames(tmp_fbook)==c("entry")] <- c("entry_id")
    
    if(sum(is.na(tmp_fbook$entry))>1){ #removing extra plots with no entries
      if(opt$fillGap){
        tmp_fbook$entry[is.na(tmp_fbook$entry)] <- "filler"
      } else {
        tmp_fbook <- tmp_fbook[-c(min(which(is.na(tmp_fbook$entry))):nrow(tmp_fbook)),]}
    }
    
    tmp_fbook <- tmp_fbook[,c("occurrence","plot_number","replicate","entry_id","field_row","field_col")]
    
    trials[[i]]$book <- tmp_fbook
  }
}

# create one design array with all occurrences
DesignArray <- trials[[1]]$book
if(opt$nTrial>1){
  for(i in 2:opt$nTrial){
    DesignArray <- rbind(DesignArray,trials[[i]]$book)
  }
}

# save the Design Array to a csv file
write.csv(DesignArray, file = paste(paste(opt$outputPath, opt$outputFile, sep = "/"), "_DesignArray.csv", sep = ""), row.names = FALSE)