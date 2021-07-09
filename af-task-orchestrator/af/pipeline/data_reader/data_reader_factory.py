from af.pipeline.data_reader.exceptions import DataSourceNotAvailableError
from af.pipeline.data_reader.models.enums import DataSource
from af.pipeline.data_reader.phenotype_data import PhenotypeData
from af.pipeline.data_reader.phenotype_data_brapi import PhenotypeDataBrapi
from af.pipeline.data_reader.phenotype_data_ebs import PhenotypeDataEbs


class DataReaderFactory:
    """Factory to get phenotype data based on api data source"""

    def __init__(self, data_source: DataSource):
        """Constructs a data reader factory for given data source.

        Args:
            DataSource enum. eg., Datasource.EBS or DataSource.BRAPI
        """
        self.data_source = data_source

    def get_phenotype_data(self, **kwargs) -> PhenotypeData:
        """Returns an interface for reading phenotype data.

        Args:
            kwargs: Key word arguments for phenotype data.

        Returns:
            A concretae phenotype object for the datasource selected.

        Raises:
            NotImplementedError: If the abstract method in the interface is not
            implemented  by the concrete class.
        """
        if self.data_source == DataSource.EBS:
            return PhenotypeDataEbs(**kwargs)
        elif self.data_source == DataSource.BRAPI:
            return PhenotypeDataBrapi(**kwargs)
        else:
            raise DataSourceNotAvailableError

    def get_genotype_data(self, **kwargs):
        raise NotImplementedError
