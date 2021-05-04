
"""
To manage module imports when run in slurm or imported into celery task,
pipeline python scripts should append parent directory to sys path,
so pipeline as a module can be imported by both celery task and slurm script.
"""
import os
import sys

import re

currentdir = path.dirname(os.path.realpath(__file__))
parentdir = path.dirname(currentdir)
sys.path.append(parentdir)

from pipeline.dpo import ProcessData  # noqa: E402

from pipeline.database.core import SessionLocal  # noqa: E402

from pipeline.database.models import Job  # noqa: E402


class Analyze:
    """ Runs asreml analysis engine.
    """

    def __init__(
            self,
            data_source: str,
            api_base_url: str,
            api_token: str,
            analysis_request,
            analysis_config,
            output_folder):
        """ Constructor.

        Args:
            data_source: type of API data source EBS/BRAPI.
            api_base_url: Base url for api
            api_token: Access token for the API
        """
        self.process_data = ProcessData(data_source, api_base_url, api_token)
        self.db_session = SessionLocal()

    def _get_job_engine(self):
        engine = self.analysis_request['metadata']['engine']
        engine = re.sub("-.*", "", engine)
        return engine.lower()

    def run(self, analysis_request, analysis_config, output_folder):

        request_id = analysis_request["metadata"]["id"]

        engine = self._get_job_engine()

        job_input_files = pd.run(analysis_request, analysis_config, output_folder)

        for job_input_file in job_input_files:
            # TODO: Call analytical job engine
            pass


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process input data to feed into analytical engine')

    parser.add_argument('--request_file', help='File path for analysis request')
    parser.add_argument('--config_file', help='File path for analysis config')
    parser.add_argument('--output_folder', help='Directory to write output files')

    parser.add_argument('--datasource_type', help='Datasource to use EBS or BRAPI')
    parser.add_argument('--api_url', help='Api base url for data source to download input data from')
    parser.add_argument('--api_token', help='Api token to access datasource api')

    args = parser.parse_args()

    if path.exists(args.request_file):
        with open(args.request_file) as f:
            analysis_request = json.load(f)
    else:
        raise InvalidAnalysisRequest(f"Request file {args.request_file} not found")

    if path.exists(args.config_file):
        with open(args.config_file) as f:
            analysis_config = json.load(f)
    else:
        raise InvalidAnalysisConfig(f"Request file {args.config_file} not found")

    if not path.exists(args.output_folder):
        raise ProcessDataException(f"Output folder {args.output_folder} not found")

    Analyze(
        args.datasource_type,
        args.api_url,
        args.api_token,
        analysis_request,
        analysis_config,
        output_folder
    ).run()
