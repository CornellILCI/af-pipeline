from rpy2.robjects.packages import importr
import rpy2.robjects as robjects


script = '''
library(asreml)

# just using the example data
data <- read.csv("{datafile}",h=T)

# Some cata modification required by asreml (do not care with this now)
data <- data[with(data, order(row,col)),]
data$rep <- as.factor(data$rep)
data$row <- as.factor(data$row)
data$col <- as.factor(data$col)
data$entry <- as.factor(data$entry)

# stat model (the pipeline will provide this from the ba)
# here is where asreml is really executed
asr <- asreml(fixed = {fixed_formula},
              random = {random_formula},
              residual = {residual_formula},
              data = data)

#requested result
#asreml generates many results, stored in the object we called asr, lets consider that we want the predictions 
pred<-predict(asr,classify="entry")$pvals

#printing the results in a csv (we may not do this way in our pipeline)
write.csv(pred, file = "{result1}",quote=F,row.names=F)

'''

def run_asreml_1():
    
    datafile = "testdata/data.csv"
    fixed_formula = "AYLD_CONT ~  rep + row + col"
    random_formula = "~ entry"
    residual_formula = "~ar1(row):ar1(col)"
    result1 = "testdata/results_example.csv"

    user_script = script.format(datafile=datafile, fixed_formula=fixed_formula, random_formula=random_formula, residual_formula=residual_formula, result1=result1)

    robjects.r(user_script)  # quickest way to implement, but might be hard to get error desc....



def run_asreml_2():
    from rpy2.robjects import Formula

    asremlr = importr('asreml')
    base = importr('base')

    data = robjects.r['read.csv']("testdata/data.csv", True)

    #have to do this because i haven't figured out how to do the sorting in rpy2
    robjects.globalenv['data'] = data
    robjects.r("data <- data[with(data, order(row,col)),]")

    data = robjects.globalenv['data']
    # get the indeces of the columns
    rep = data.colnames.index('rep')
    row = data.colnames.index('row')
    col = data.colnames.index('col')
    entry = data.colnames.index('entry')

    data[rep] = base.as_factor(data[rep])
    data[row] = base.as_factor(data[row])
    data[col] = base.as_factor(data[col])
    data[entry] = base.as_factor(data[entry])

    fixed = Formula("AYLD_CONT ~  rep + row + col")
    random = Formula("~ entry")
    residual = Formula("~ar1(row):ar1(col)")

    asr = asremlr.asreml(fixed=fixed, random=random, residual=residual, data=data)

    # This one produces an error i cannot decode, 
    # pr = asremlr.predict_asreml(asr, classify="entry") 

    #but if i run it this way it will be successful
    robjects.globalenv['asr'] = asr
    robjects.r('pred<-predict(asr,classify="entry")$pvals')
    pred = robjects.globalenv['pred']

    robjects.r['write.csv'](pred, file="testdata/resuls_example.csv")







