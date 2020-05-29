  #!/usr/bin/Rscript
  packages_root <- paste(Sys.getenv("EBSAF_ROOT"), "models/packages", sep='/')
  ##==================================================##
  ##==================================================##
  ##		Package: optparse		    ##
  ##==================================================##
  ##==================================================##
  
  #dependencies of optparse ([methods], getopt >= 1.20.2)
  getOpt <- paste(packages_root, "getopt_1.20.2.tar.gz", sep="/") 
  install.packages(getOpt, repos=NULL, type="source")
  
  optParse <- paste(packages_root, "optparse_1.6.4.tar.gz", sep="/")
  install.packages(optParse, repos=NULL, type="source")
  ##==================================================##
  ##end for Package: optparse
  ##==================================================##
  
  ##==================================================##
  ##==================================================##
  ##		Package: agricolae		    ##  
  ##==================================================##
  ##==================================================##
  
  #dependencies of agricolae (klaR,AlgDesign)
  
  #dependencies of klaR (combinat, questionr)
  # combinat <- paste(packages_root, "combinat_0.0-8.tar.gz", sep="/") 
  # install.packages(combinat, repos=NULL, type="source")
  # 
  #dependencies of questionr (rstudioAPI, miniUI, shiny, classInt, labelled)
  #
  # rstudioapi <- paste(packages_root, "rstudioapi_0.11.tar.gz", sep="/") 
  # install.packages(rstudioapi, repos=NULL, type="source")
  #
  #dependencies of miniUI (shiny)
  #
  #dependendies of shiny (ctable, jsonlite, promises, httpuv, sourcetools, later, fastmap)
  #
  # shiny <- paste(packages_root, "shiny_1.4.0.2.tar.gz", sep="/") 
  # install.packages(shiny, repos=NULL, type="source")
  # 
  # miniui <- paste(packages_root, "miniUI_0.1.1.1.tar.gz", sep="/") 
  # install.packages(miniui, repos=NULL, type="source")
  # 
  # 
  # calssint <- paste(packages_root, "classInt_0.4-3.tar.gz", sep="/") 
  # install.packages(calssint, repos=NULL, type="source")
  # 
  # labelled <- paste(packages_root, "labelled_2.4.0.tar.gz", sep="/") 
  # install.packages(labelled, repos=NULL, type="source")
  # 
  # questionr <- paste(packages_root, "questionr_0.7.0.tar.gz", sep="/") 
  # install.packages(questionr, repos=NULL, type="source")
  # 
  # klaR <- paste(packages_root, "klaR_0.6-15.tar.gz", sep="/") 
  # install.packages(klaR, repos=NULL, type="source")
  
  #dependencies of AlgDesign ()
  # algdesign <- paste(packages_root, "AlgDesign_1.2.0.tar.gz", sep="/") 
  # install.packages("AlgDesign", repos=NULL, type="source")
  # 
  # agricolae <- paste(packages_root, "agricolae_1.3-2.tar.gz", sep="/") 
  # install.packages(agricolae, repos=NULL, type="source")
  
  ##==================================================##
  ##end for Package: agricolae
  ##==================================================##
    
  ##==================================================##
  ##==================================================##
  ##		Package: ebsRtools		    ##
  ##==================================================##
  ##==================================================##
  
  ebsRtools <- paste(packages_root, "ebsRtools_0.2.0.tar.gz", sep="/") 
  install.packages(ebsRtools, repos=NULL, type="source")
  
  ##==================================================##
  ##end for Package: ebsRtools
  ##==================================================##