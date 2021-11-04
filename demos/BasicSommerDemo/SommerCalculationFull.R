## Default repo
local({r <- getOption("repos")
       r["CRAN"] <- "https://cloud.r-project.org" 
       options(repos=r)
})

#####################################################################################################################
#JSON Integration
library("rjson")
#read command line args
args = commandArgs(trailingOnly=TRUE)
#confirm that there is exactly 1 arg
if (length(args)!=1) {
  stop("Run this with exactly 1 parameter. (JSON file name)", call.=FALSE)
}


writeLines("Reading args[1]")
#reads JSON
jsonInput <- fromJSON(file = args[1])
#confirm that the file showed up

print(jsonInput)

#######simulate a population
# nChrom <- if("nChrom" %in% names(jsonInput)) jsonInput$nChrom else 10                       # number of chromosomes
# nLoci <- if("nLoci" %in% names(jsonInput)) jsonInput$nLoci else 100                         # number of loci per chromosome
stopifnot(
    "input_phenotypic_data" %in% names(jsonInput),
    "grm" %in% names(jsonInput),
    "output_var" %in% names(jsonInput),
    "output_statmodel" %in% names(jsonInput),
    "output_BV" %in% names(jsonInput),
    "output_pred" %in% names(jsonInput),
    "output_yhat" %in% names(jsonInput),
    "output_outliers" %in% names(jsonInput),
    "fixed" %in% names(jsonInput),
    "random" %in% names(jsonInput),
    "rcov" %in% names(jsonInput)
)

input_phenotypic_data <- if("input_phenotypic_data" %in% names(jsonInput)) jsonInput$input_phenotypic_data else ''
grm <- if("grm" %in% names(jsonInput)) jsonInput$grm else ''
output <- if("output" %in% names(jsonInput)) jsonInput$output else ''

#####################################################################################################################


#install.packages('sommer')
library(sommer)
#install.packages('gtools')
library(gtools)

# Phenofounders <- read.csv('/Users/sb2597/Documents/TestPythonToR/Sommer ILCI code/Phenofounders.csv', header=T)
Phenofounders <- read.csv(input_phenotypic_data, header=T)

head(Phenofounders)
# A <- read.table('/Users/sb2597/Documents/TestPythonToR/Sommer ILCI code/GRM.txt', header = T)
A <- read.table(grm, header = T)
A <- as.matrix(A)
A[1:10,1:10]
Phenofounders$ID <- colnames(A) ## this is just to make the ID of the phenotype data and the row/column name on the GRM are the same
#Phenofounders$rep <- rep

# mix1 <- mmer(Phenotype~rep,
#              random=~vs(ID, Gu=A),	     #ID is the ID of the hybrids
#              rcov=~ units,		             #this is for the residuals and its always 'units'
#              data=Phenofounders)

# mix1 <- mmer(fixed = jsonImput$fixed,
#              random =~vs(ID, Gu=A),	     #ID is the ID of the hybrids
#              rcov =~ units,		             #this is for the residuals and its always 'units'
#              data = Phenofounders)


sommerModel <-paste("mix1 <- mmer(fixed=", jsonInput$fixed, ",\n", 
          "random=", jsonInput$random, ",\n", 
          "rcov=", jsonInput$rcov, ",\n",
          "data=Phenofounders)",
          sep = "")

eval(parse( text=sommerModel ))


summary_model <- summary(mix1)

#asr
variances <- as.data.frame(summary_model$varcomp)
write.csv(variances, file=jsonInput$output_var, row.names = T, quote=F)

stat_model <- summary_model$logo
write.csv(stat_model, file=jsonInput$output_statmodel, row.names = F, quote=F)

#pvs
predSommer <- predict.mmer(object=mix1, classify = "ID")
predictions <- predSommer$pvals
write.csv(predictions, file=jsonInput$output_pred, row.names = F, quote=F)

#sln
BVs <- as.data.frame(mix1$U$`u:ID`$Phenotype) # $EBS effects asreml sln
colnames(BVs) <- "breeding.value"
BVs.std.error <- sqrt(diag((mix1$PevU$`u:ID`$Phenotype)))
BVs <- data.frame(ID = rownames(BVs),BVs,std.error = BVs.std.error)
write.csv(BVs, file=jsonInput$output_BV, row.names = F, quote=F)

#yhat
Yhat <- mix1$fitted
Residuals <- mix1$residuals
Hat <- diag(mix1$P)
fitted <- as.data.frame(cbind(Yhat,Residuals,Hat))
colnames(fitted) <- c("Yhat","Residuals","Hat")
write.csv(fitted, file=jsonInput$output_yhat, row.names = F, quote=F)

#outliers
out <- boxplot.stats(Residuals)$out
if(length(out)>0){
  outliers <- Phenofounders[Residuals%in%out,]
  rownames(outliers)
  write.csv(outliers, file=jsonInput$output_outliers, row.names = F, quote=F)
}

## printing results