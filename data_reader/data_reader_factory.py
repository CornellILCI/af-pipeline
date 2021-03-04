from models.enums import DataSource

from data_reader.phenotype_data_ebs import PhenotypeDataEbs
from data_reader.phenotype_data_brapi import PhenotypeDataBrapi


class DataReaderFactory:
    """ Facoty to get phenotype data based on api data source
    """

    def __init__(self, data_source: DataSource):
        self.data_source = data_source

    def get_pheotype_data(self, **kwargs):
        if self.data_source == DataSource.EBS:
            return PhenotypeDataEbs(**kwargs)
        elif self.data_source == DataSource.BRAPI:
            return PhenotypeDataBrapi(**kwargs)
        else:
            raise NotImplementedError
