library(sommer)
# install with install.packages('sommer')

#NOTE: library or require could be used
# But require will not raise an error if a package is not found
# library on the other hand will fail early.


# input files will be read from:
#    ${PWD}/input
# all output files will be correspondingly written to:
#    ${PWD}/output

# reading phenotype matrix data file and the matrix 
# it was named "DT.dat" on email, but it was converted
# to csv
# read.table is used as well
#Pheno <- read.csv('input/Phenogenotyped.csv', header=T)

#A <- read.table('A.txt', header=F) #and here too
#A <- read.table('input/A.txt', header=T) #and here too
#A <- as.matrix(A)
#DT <- Pheno

calculate <- function(Pheno, A) {
    head(Pheno)
    A <- as.matrix(A)
    DT <- Pheno
    # do we sanity check, for dimensions?
    # pheno_dims <- dim(DT) 
    # adims <- dim(A) 

    # check if output directory exists
    if (!dir.exists('output')) {
        dir.create('output')
    }

    cat("Running single trait model...\n-->Formula: Yield~Rep\n")
    #singe trait model
    mix1 <- mmer(Yield~Rep,
                random=~vs(ID, Gu=A),	#ID is the ID of the hybrids
                rcov=~units,		#this is for the residuals and its always 'units'
                data=DT)

    # This is how we access some of the results from the model. 
    # summary(mix2)$varcomp #this is how you access the (co)variances
    # GEBV <- as.data.frame(mix1$U$`u:ID`$Yield) #and this is how you access the breeding values

    # Saving the cov and breeding value results as a variables.
    results_mix1.covariances <- summary(mix1)$varcomp #this is how you access the (co)variances
    results_mix1.GEBV <- as.data.frame(mix1$U$`u:ID`$Yield) #and this is how you access the breeding values

    # Use code below if you want to store the values to a text file
    # Other options are possible.
    write.csv(results_mix1.covariances , "output/results_mix1.covariances.csv")
    write.csv(results_mix1.GEBV , "output/results_mix1.breeding_values.csv")


}