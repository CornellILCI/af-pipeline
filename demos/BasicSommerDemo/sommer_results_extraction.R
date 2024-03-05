#suppressWarnings(suppressPackageStartupMessages(library(ebsRtools)))
suppressWarnings(suppressPackageStartupMessages(library(dplyr)))
suppressWarnings(suppressPackageStartupMessages(library(sommer)))
#suppressWarnings(suppressPackageStartupMessages(library(AGHmatrix)))

# To simulate data of an experiment (field trial)
nInd <- 20 # number of entries (germplasm, varieties, hybrids, lines, entries...)
rep <- 2
nLoc <- 2
entry_id <- c(1:nInd)

trials <- list()
for(i in c(1:nLoc)){
  tmp <- ebsRtools::randRCBD(trt = entry_id, r = rep)
  tmp$book$occurrence <- i
  trials[[i]] <- tmp
}

trials <- ebsRtools::add.layout(trials,nFieldRow = nInd/10)

if(nLoc>1){
  l <- list()
  for(i in 1:nLoc){
    l[[i]]<-trials[[i]]$book
  }
  trials <- rlist::list.rbind(l)
}

trials$occurrence <- as.factor(trials$occurrence)
trials$field_row <- as.factor(trials$field_row)
trials$field_col <- as.factor(trials$field_col)
trials$plot_number <- as.factor(trials$plot_number)

m <- 15
d <- 6

portion <- c(0.35,#plot
             0.1,#rep
             0.45,#entry
             0.1,#blk
             0.12,#occ
             0.00,#row
             0.00,#col
             0.18)#gxe
sum(portion)
sd <- portion*d

#simulating
simu <- function(trial,m,sd,g=NULL){
  if(!is.null(g)){
    if(length(g)!=nlevels(trial$entry_id)) stop("g should have the same levels of entry_ids")
  }
  tmp <- trial %>% mutate(
    replicate = factor(paste(occurrence,replicate, sep = "_")),
    field_row = factor(paste(occurrence,field_row, sep = "_")),
    field_col = factor(paste(occurrence,field_col, sep = "_")),
    plot_number = factor(paste(occurrence,plot_number, sep = "_")),
    gxe = factor(paste(occurrence,entry_id,sep = "_"))
  )
  if("block"%in%colnames(tmp)){
    tmp <- tmp %>% mutate(
      block = factor(paste(occurrence,replicate,block, sep = "_")),
    )
  } else {
    sd <- sd[-4]
  }
  for(i in 1:ncol(tmp)){
    if(!exists("a")){
      a <- c()
    }
    a <- c(a,is.factor(tmp[,i]))
  }
  nfac <- sum(a)
  rm(a)
  levelsFactors <- rep(NA,nfac)
  tables <- list()
  for(i in (1:ncol(tmp))){
    levelsFactors[i] <- nlevels(tmp[,i])
    a <- data.frame(
      fac = unique(tmp[,i]),
      coef = if(!is.null(g) & colnames(tmp)[i]=="entry_id"){
        g
      }else{rnorm(levelsFactors[i],0,sd[i])}
      )
    tables[[i]] <- a
    names(tables)[i] <- colnames(tmp)[i]
  }
  
  composeY <- matrix(NA,nrow(tmp),length(tables))
  for (i in 1:length(tables)){
    composeY[,i]<-tables[[i]]$coef[match(tmp[,i],tables[[i]]$fac)]
  }
  trialData <- trial
  trialData$y <- rowSums(composeY,na.rm = T) + m
  b<-list(trialData,tables)
  b
}

sim_data <- simu(trial = trials,
                 m = m,
                 sd = sd,
                 g=NULL)

sim_effects <- sim_data[[2]]
Phenofounders <- sim_data[[1]][sim_data[[1]]$occurrence==1,]%>%droplevels
colnames(Phenofounders) <- c("plot","rep","ID","loc","row","col","Phenotype")

## Simulating genetic markers
nMar <- 6000 # number of markers (if simulate also genomic info)
freq <- c(0.3,0.5,0.4)

M <- matrix(rbinom(n=nInd*nMar,size=2,prob=sample(freq,1)),nInd,nMar)
colnames(M) <- paste("M",c(1:nMar), sep="")
rownames(M) <- c(1:nInd)
#hist(M, main = "freq of genotypes", xlab = "genotypes")
#M[1:10,1:10]

### Creating the GRM
A <- AGHmatrix::Gmatrix(M,
                        method="VanRaden",
                        missingValue=-9,
                        maf=0.05)


## Fitting mixed model in sommer to execute the analysis
mix1 <- mmer(Phenotype~1,# + rep,
             random=~ vs(ID, Gu=A),	     #ID is the ID of the hybrids $EBS entry_id
             rcov=~units,		             #this is for the residuals and its always 'units' # Only units if no modelling any var-cor-covar error structure
             data=Phenofounders)

summary_model <- summary(mix1)

#asr
variances <- as.data.frame(summary_model$varcomp)
stat_model <- summary_model$logo

#pvs
predSommer <- predict.mmer(object=mix1, classify = "ID")
predictions <- predSommer$pvals

#sln
BVs <- as.data.frame(mix1$U$`u:ID`$Phenotype) # $EBS effects asreml sln
colnames(BVs) <- "breeding.value"
BVs.std.error <- sqrt(diag((mix1$PevU$`u:ID`$Phenotype)))
BVs <- data.frame(ID = rownames(BVs),BVs,std.error = BVs.std.error)

#yhat
Yhat <- mix1$fitted
Residuals <- mix1$residuals
Hat <- diag(mix1$P)
fitted <- as.data.frame(cbind(Yhat,Residuals,Hat))
colnames(fitted) <- c("Yhat","Residuals","Hat")

#outliers
out <- boxplot.stats(Residuals)$out
if(length(out)>0){
  outliers <- Phenofounders[Residuals%in%out,]
  rownames(outliers)
}

## printing results
write.csv(variances, file='output_var', row.names = T, quote=F)
write.csv(stat_model, file="output_statmodel", row.names = F, quote=F)
write.csv(BVs, file="output_BV", row.names = F, quote=F)
write.csv(predictions, file="output_pred", row.names = F, quote=F)
write.csv(fitted, file="output_yhat", row.names = F, quote=F)
write.csv(outliers, file="output_outliers", row.names = F, quote=F)
