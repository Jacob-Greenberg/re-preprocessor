import abc

class Extractor(abc.ABC):
    @abc.abstractmethod
    def extract_file(self, source_path: str, dest_path: str) -> bool:
        """
        :source_path: the path to the file which is to be extracted
        :dest_path: the path where the results of the extraction should be placed
        :returns: true on success, false otherwise
        """
        pass
