import csv
import json
import os

from pandas import DataFrame

from af.pipeline.db import services
from af.pipeline.db.core import DBConfig
from af.pipeline.dpo import ProcessData
from af.pipeline.job_data import JobData
from af.pipeline import data_reader
from af.pipeline.data_reader import GenotypeData
from af.pipeline.data_reader.models.brapi.genotyping import VariantSet, AlleleMatrixDataMatrices, AlleleMatrix, Variant, CallSet, Sample

def getVariantDbId(v:VariantSet) -> str:
    return v.variantSetDbId

def getCallsetSampleId(c:CallSet) -> str:
    return c.sampleDbId

def getSampleName(s:Sample)->str:
    return s.sampleName

def getVariantNamesFromIds(ids:'list[str]',geno_reader:GenotypeData)->'list[str]':
    retlist=[]
    variants:list[Variant] = geno_reader.get_variant(ids)
    for variant in variants:
        retlist.extend(variant.variantNames[0])#First name is fine
    return retlist    

def getSampleNamesFromCallsetIds(ids:'list[str]',geno_reader:GenotypeData)->'list[str]':
    callsets:list[CallSet]=geno_reader.get_callsets(callSetDbIds=ids)
    sampleIds=list(map(getCallsetSampleId,callsets)) 
    samples:list[Sample] = geno_reader.get_samples(sampleDbIds=sampleIds)
    sampleNames=list(map(getSampleName,samples))
    return sampleNames

def getVariantName(v:Variant) -> str:
    return v.variantNames

def homozygoteToDosage(homozygote:str)->str:
    count = 0
    if len(homozygote) !=3: return homozygote #Pass back NA/. unchanged 
    firstChar = homozygote[0]
    lastChar = homozygote[-1]
    if(firstChar == "0"):count=count+1
    if(lastChar == "0"):count=count+1
    return str(count)

def getGenoMatrices(mats:'list[AlleleMatrix]')->'list[AlleleMatrixDataMatrices]':
    return list(map(getGenoMatrix,mats))

def getGenoMatrix(mat:AlleleMatrix)->AlleleMatrixDataMatrices:
    for dmat in mat.dataMatrices:
        if dmat.dataMatrixAbbreviation == "GT":
            return dmat
    return None

#strFmtFunction is a string formatting function str->str... no idea how to code that type hint - JDLS
def formatGenoData(mats:'list[AlleleMatrixDataMatrices]',strFmtFunction)->'list[list[str]]':
    retlist=[] #single matrix
    
    for gmat in mats:
        genoMat = gmat.dataMatrix
        #fmtGenoMat=map(map(strFmtFunction),genoMat) Nope -JDLS
        fmtGenoMat=[list(map(strFmtFunction,subList)) for subList in genoMat] #StackOverflow second best comment? https://stackoverflow.com/questions/34080828/map-a-nested-list-in-python
        if(len(retlist)==0):retlist=fmtGenoMat
        else: retlist.extend(fmtGenoMat)

    return retlist


def getCallList(mat:AlleleMatrix):
    return mat.callSetDbIds


def getAllVariantsList(mats:'list[AlleleMatrix]')->'list[str]':
    retlist=[]
    for mat in mats:
        retlist.extend(mat.variantDbIds)
    return retlist
    
def getVariantList(mat:AlleleMatrix):
    return mat.variantDbIds
        

class SommeRProcessData(ProcessData):


    
    def __init__(self, analysis_request):
        super().__init__(analysis_request)

    def __get_job_name(self):
        # TODO: put this in ProcessData
        return f"{self.analysis_request.requestId}"

    def sesl(self):
        """Preprocess input data for SommeR Analysis"""

        jobs = []

        for occurrence_id in self.occurrence_ids:

            for req_trait in self.analysis_request.traits:

                trait: data_reader.models.Trait = data_reader.models.Trait(
                    trait_id=req_trait.traitId, trait_name=req_trait.traitName, abbreviation=req_trait.traitName
                )

                # pre process input job data
                plots = self.data_reader.get_plots(occurrence_id=occurrence_id)
                plot_measurements = self.data_reader.get_plot_measurements(
                    occurrence_id=occurrence_id, trait_id=trait.trait_id
                )

                plots_measurements = plots.merge(plot_measurements, on="observationUnitDbId", how="left")

                plots_measurements = self.format_input_data(plots_measurements, trait)
                
                if self.geno_data_reader is not None:
                    variant_sets:list=self.geno_data_reader.get_variantsets(self.analysis_request.genoStudyIds)
                    allele_matrices:list[AlleleMatrix]=self.geno_data_reader.post_search_allelematrix(variantSetDbIds=list(map(getVariantDbId,variant_sets)), expandHomozygotes=True)
                    callsetIds=allele_matrices[0].callSetDbIds
                    variantIds=[]
                    for mat in allele_matrices: variantIds.extend(mat.variantDbIds) #we're assuming the same calls on every matrixfor now
                    variantNameList = getVariantNamesFromIds(ids=variantIds,geno_reader=self.geno_data_reader) #markers
                    sampleNameList = getSampleNamesFromCallsetIds(ids=callsetIds,geno_reader=self.geno_data_reader) #plants
                    allele_matrix = DataFrame(data=formatGenoData(allele_matrices,homozygoteToDosage), index=sampleNameList,columns=variantNameList)
                    
                    #TODO - make into a GRM when needed - when is it needed?
                    #For now, lets just see if it works
                    
                    
                    #mergeHow=self.analysis_request.genoConnectionAction
                    #validateMerge=None
                    #if mergeHow == "fail":
                    #    validateMerge="1:1"
                    #    mergeHow="full"
                        
                    #plot_measurements = plot_measurements.merge(right=allele_matrix,left_on="germplasm",right_index=True,how=mergeHow,validate="1:1")#Keep all pheno info, only keep geno info that relates
                
                job_name = f"{self.analysis_request.requestId}_{occurrence_id}_{trait.trait_id}" 
                job = JobData(
                    job_name=job_name,
                    trait_name=trait.trait_name,
                    job_result_dir=self.get_job_folder(job_name)
                )

                data_file_path = os.path.join(job.job_result_dir, f"{job.job_name}.csv")
                allele_matrix.to_csv(data_file_path + ".geno", index=False)#write a geno file
                plots_measurements.to_csv(data_file_path, index=False)

                job.data_file = data_file_path
                
                self._set_job_params(job, trait)

                jobs.append(job)
        return jobs

    def seml(self):
        pass

    def mesl(self):
        raise NotImplementedError

    def meml(self):
        raise NotImplementedError
