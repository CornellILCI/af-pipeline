

from af.pipeline.job_data import JobData, JobParams
from af.pipeline.asreml_r import analyze
data = JobData()
params = JobParams()
params.formula = "fixed = {trait_name} ~ rep, random = ~ ge"
params.residual = "~ units"
data.job_params = params
data.trait_name = "AYLD_CONT"
data.job_name="test-job"
data.job_result_dir="/tmp"
data.data_file="/tmp/test-data.csv"
analyze.run_asremlr("/tmp", data)