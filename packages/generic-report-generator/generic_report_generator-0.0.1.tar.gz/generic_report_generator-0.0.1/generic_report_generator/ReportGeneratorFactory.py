from abc import ABC, abstractmethod

from sqlformat import ResultPersistenceStrategy

from .DropTempTableStrategy import DropTempTableStrategy
from .ResultDownloadStrategy import ResultDownloadStrategy

class ReportGeneratorFactory(ABC):
    @abstractmethod
    def persistence_strategy(self, *args, **kwargs) -> ResultPersistenceStrategy:
        pass

    @abstractmethod
    def drop_all_temp_table_strategy(self, *args, **kwargs) -> DropTempTableStrategy:
        pass

    @abstractmethod
    def result_download_strategy(self, *args, **kwargs) -> ResultDownloadStrategy:
        pass
