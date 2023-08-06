from abc import ABC, abstractmethod

from sqlalchemy.engine import Engine
from sqlformat import ResultPersistenceStrategy

from .DropTempTableStrategy import DropTempTableStrategy
from .ResultDownloadStrategy import ResultDownloadStrategy

class ReportGeneratorFactory(ABC):
    @abstractmethod
    def sa_engine(self, connection_dialect, *args, **kwargs) -> Engine:
        pass

    @abstractmethod
    def persistence_strategy(self, *args, **kwargs) -> ResultPersistenceStrategy:
        pass

    @abstractmethod
    def drop_all_temp_table_strategy(self, *args, **kwargs) -> DropTempTableStrategy:
        pass

    @abstractmethod
    def result_download_strategy(self, *args, **kwargs) -> ResultDownloadStrategy:
        pass
