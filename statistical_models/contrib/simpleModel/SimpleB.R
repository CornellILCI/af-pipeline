#########################SIMPLE MODEL v1.1##########################################################
##############  20170308-water stress                                                     ##########
#######  By Bing Liu, ABE, University of Florida ------  2017-04-27                       ##########
#######  Updated by Liujun Xiao,ABE, University of Florida ------  2017-06-08             ##########
#######  Adding PET function by Kwang Soo Kim, Seoul National University ------2017-06-08  ##########
#######  Recoding by Liujun Xiao,ABE, University of Florida ------ 2018-03-09             ##########
####################################################################################################


####################################################################################################
#######		Six Steps for adding a new crop       			             ###############
#######		                         					     ###############
#######   1. Prepare the model inputs in Treatment.csv 
#######     Crop,Exp,Trt,weather,lat,Elev,CO2,sowingDate,
#######	    irrigation=irrigation ID in irrigation table: must be identical to Trt in irrigation.csv table, if no irri=0
#######	    AWC=DUL-LL (e.g. from DSSAT soil)
#######     RCN=runoff number (DSSAT:SLRO)
#######  	DDC=deep drainage coeff (DSSAT:SLDR)
####### 	WUC=water uptake coeff (use default=0.096)
#######  	RZD=root depth in mm)
#######  	Water=switch (yes=use rainfall and irri table; no for no water stress)
#######  	set following parameter to overwrite in R code: Tsum,	HI,	I50A,	I50B,
#######  	NOTE-to leave some notes
####### 
#######  2. prepare irrigation table
#######  	file: irrigation.csv        IRVAL=irrgation in mm per specific date
#######
#######  3. Prepare weather file
#######   	if from DSSAT
#######          *WEATHER : AUCB
#######          @ INSI      LAT     LONG  ELEV   TAV   AMP REFHT WNDHT
#######          AUCB   -35.00   149.00     0  17.0   7.0   -99   -99
#######          DATE  SRAD  TMAX  TMIN  RAIN         # data must start as line 4 and remove "@" here
#######   
#######          or CSV with same headers
#######
#######   4. Add a new parameter list in [Crop Parameter List] (copy and rename to new crop below) 
#######
#######   5. Add a selection case in [copy Crop Parameter Selection near line 610]
#######  	if(treat$Crop[1]=="potato"){para<-potatoPara}; ---> copy and rename to new crop
#######
#######   6. Add obs data
#######     copy: @TRNO	DATE	UYAD	LAID
#######     Extend to: TRNO	DATE	DAP	GWAD	LAID	fSolar	CWAD    ###### DAP=day fater planting=DATE-sowing_date
#######     GWAD=yield
#######     CWAD=total above ground + yield (no roots)    #### must hav at least 1 data/trt
#######     fSolar=1-EXP(-k*LAI)
#######     delate Date and LAID
#######     save file as Obs_crop_name_exp_name.csv
#######
#######
####################################################################################################
####################################################################################################

#################  load R packages --- needs to stay here 
rm(list=ls())   #### cleans memory - needs to saty here
############  Gridcell Simulation Switch  ##########################################################
GridsimulationSwitch=c('OFF','ON')[1]  
########1=single point simulation, 2= Grid cell simulation


###########load packages######################################################################
list.of.packages <- c("ggplot2", "plyr","parallel")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)

library(ggplot2)
library(plyr)
library(parallel)
if(dev.cur()>1){replicate(dev.cur()-1,dev.off())} 
setwd(script.dir <- dirname(sys.frame(1)$ofile)) #### Relative working directory
setwd("C:/Users/DPEQUENO/Documents/CIMMYT/2019/SIMPLE Model/SimpleB/SIMPLE20181102")  ########Absolute working directory
source("Mainfunction.R")
######weather directory for regional simulation###
WeatherDir="./Gridcell Weather/historical/"

######weather type option########################
WeatherType=c("WTH","CSV","Rdata")[1]

#########Intput map##########################
MapExtention=c("World","United States of America","China","Canada","Brazil","...")[2]
SimulatingYear=c(2001:2002)

########## Output option################
DailyOutputforgridcell=c('OFF','ON')[2]
DailyOutputOutput=c("Crop","Exp","Label","Trt","Day","DATE","Tmax","Tmin","Radiation",
                    "TT","fSolar","Biomass","dBiomass","HI","Yield","F_Temp","F_Heat",
                    "F_Water","ARID","I50B","I50A","ETO","MaturityDay")
MapoutputYear=2001


############  Model starts here  ##################################################################
############  Read inputs - treatments, soil weather, CO2
if(GridsimulationSwitch=='OFF'){
  management<-read.table("./Input/Simulation Management.csv",header=TRUE,sep=",",stringsAsFactors=FALSE)
  treatment<-read.table("./Input/Treatment.csv",header=TRUE,sep=",",stringsAsFactors=FALSE);treatment$Species.=tolower(treatment$Species.)
  cultivar<-read.table("./Input/Cultivar.csv",header=TRUE,sep=",",stringsAsFactors=FALSE);cultivar$Species.=tolower(cultivar$Species.)
  irri<-read.table("./Input/Irrigation.csv",header=TRUE,sep=",",stringsAsFactors=FALSE);irri$Species.=tolower(irri$Species.)
  soil<-read.table("./Input/Soil.csv",header=TRUE,sep=",",stringsAsFactors=FALSE)  
  para_spec<-read.table("./Input/Species parameter.csv",header=TRUE,sep=",",stringsAsFactors=FALSE);para_spec$Species.=tolower(para_spec$Species.)
  
  ####match experiment
  management<-management[management$ON_Off==1,]
  treatment<-merge(treatment,management,by=c("Species.","Exp.","Trt."), suffixes=c("",".y"))
  treatment<-merge(treatment,soil,by="SoilName.")
  treatment<-merge(treatment,para_spec,by="Species.")
  treatment<-merge(treatment,cultivar,by=c("Species.","Cultivar."))
}else{
  treatment<-read.table("./Input/Grid_input.csv",header=TRUE,sep=",",stringsAsFactors=FALSE);treatment$Species.=tolower(treatment$Species.)
  para_spec<-read.table("./Input/Species parameter.csv",header=TRUE,sep=",",stringsAsFactors=FALSE);para_spec$Species.=tolower(para_spec$Species.)
  irri<-read.table("./Input/Irrigation.csv",header=TRUE,sep=",",stringsAsFactors=FALSE);irri$Species.=tolower(irri$Species.)
  treatment<-merge(treatment,para_spec,by="Species.")
  treatmentsingle<-treatment
  x=1:length(SimulatingYear)
  no_cores <- detectCores() - 1
  cl <- makeCluster(mc <- getOption("cl.cores", no_cores))
  clusterExport(cl, c("treatment","SimulatingYear"))
  results <- parLapply(cl,x,Treatmentplusyear) 
  stopCluster(cl)
  treatment <- do.call('rbind',results) 
}






RunModel=function(i){
  source("Mainfunction.R")
  paras=ParaInput(i)
  res<-tryCatch({SIMPLE(para=paras[c(1:3)],weather=paras$weather,ARID=paras$ARID)},error=function(e){cat("ERROR :",conditionMessage(e),"\n")})
  return(res)
}






#####Run all the experiment one by one
# x=1:nrow(treatment)
# results=list()
# if(GridsimulationSwitch=='OFF'){observations=list()}
# for (i in 1:length(x))
# {
#   results[[i]]=list()
#   source("Mainfunction.R")
#   res=RunModel(x[i])
#   results[[i]]<-res
# 
#   if(GridsimulationSwitch=='OFF'){
#     source("Obsfunction.R")
#     obs=ObsInput(x[i])
#     observations[[i]]<-obs}
# }

##########





########parallel running
t1=Sys.time() 
x=1:nrow(treatment)
no_cores <- detectCores() - 1
cl <- makeCluster(mc <- getOption("cl.cores", no_cores))
clusterExport(cl, c("treatment","irri","GridsimulationSwitch","WeatherType","WeatherDir","DailyOutputOutput"))
results <- parLapply(cl,x,RunModel) 
if(GridsimulationSwitch=='OFF')
{
  source("Obsfunction.R")
  observations<- parLapply(cl,x,ObsInput) 
}

stopCluster(cl)
Sys.time()-t1
###########

#########Simulation results reorganization
res.df <- do.call('rbind',results) 
Res_daily=ldply(res.df[,1])
Res_summary=ldply(res.df[,2])


if(GridsimulationSwitch=='OFF'){
  obs.df=do.call('rbind',observations)
  Obs_Biomass=ldply(obs.df[,1])
  Obs_FSolar=ldply(obs.df[,2])
  Obs_Yield=ldply(obs.df[,3])
  Obs_Summary=ldply(obs.df[,4])
  Obs_Summary=Obs_Summary[,c('Trt','Exp','Yield')]
  Res_Summary=merge(Res_summary,Obs_Summary,by=c('Trt','Exp'))[,c("Crop","Exp","Label","Yield.x","Yield.y","Duration","Trt")]
  names(Res_Summary)[4:5]=c("Obs_Yield","Sim_Yield")
  ##### write the simulations into files
  Yeargap=paste(unique(format(Res_summary$MaturityDay,"%Y")),collapse = "_")
  Speciesgap=paste(unique(Res_summary$Crop),collapse = "_")
  write.table(Res_daily,paste("./Output/Res_daily_",Speciesgap,"_",Yeargap,".csv",sep=""),col.names=TRUE,row.name=FALSE,sep=",")
  write.table(Res_summary,paste("./Output/Res_summary_",Speciesgap,"_",Yeargap,".csv",sep=""),col.names=TRUE,row.name=FALSE,sep=",")
  
  source("Plot.R")
  gplot(Res_daily,Res_Summary,Obs_Biomass,Obs_FSolar)
}else{
  treatmentsub=treatmentsingle[,c('Exp.','Species.','Trt.','row','col','lat')]
  Res_summary=Res_summary[,c("Exp","SowingDate","Duration","Biomass","Yield","MaturityDay")]
  Res_Summary=merge(treatmentsub,Res_summary,by.x="Exp.",by.y = "Exp")
  Yeargap=paste(unique(format(Res_Summary$MaturityDay,"%Y")),collapse = "_")
  if(DailyOutputforgridcell=='ON'){
    write.table(Res_daily,paste("./Output/Gridcell_daily_",Res_Summary$Species.[1],"_",Yeargap,".csv",sep=""),col.names=TRUE,row.name=FALSE,sep=",")
  }
  Res_Summary$MaturityYear=substr(Res_Summary$MaturityDay,1,4)
  write.csv(Res_Summary,paste0("./Output/Gridcell_summary",Res_Summary$Species.[1],"_",Yeargap,".csv"),row.names = F)
  
  Res_SummaryMap=Res_Summary[Res_Summary$MaturityYear==MapoutputYear,]
    
  source("MapPlot.R")
  
  
  Worldcountry=readRDS(file = "./Input/Map/Worldcountry.rds")
  Worldstate=readRDS(file = "./Input/Map/ne_10m_admin_1_states_provinces.rds")
  
  
  if(MapExtention=="World"){
    WMap <- Worldcountry
  }else{WMap<-Worldstate[Worldstate@data$admin==MapExtention,]
  WMap<- subset(WMap,!fips %in% c("US02", "US15", "US72"))}
  
  MapPlot(Res_SummaryMap,index="Yield",WMap,MapExtention,Title="Potato_Yield",Unit="Yield(kg/ha)")
}


