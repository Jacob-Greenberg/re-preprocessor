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

    @abc.abstractmethod
    def supported_file(self) -> str | list[str]:
        """
        :returns: a string or list of strings of the file type which the extractor can use
        e.g. "gzip" or ["tar", "tarball"]
        """
        # ex return "gzip" or return ["tar", "tarball"]
        pass

    def is_supported(self, filetype: str | list[str]) -> bool:
        """
        :filetype: the filetype to check i.e. "zip" or ".zip"
        :returns: true if the filetype is supported, false otherwise
        """
        if type(filetype) == list:
            for f in filetype:
                if f.removeprefix(".") in self.supported_file():
                    return True
            return False
        else:
            return filetype.removeprefix(".") in self.supported_file()