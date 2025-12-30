from repr_api.extractor import Extractor
from .config import SUPPORTED_FILE_TYPES
import gzip

class ExtractZIP(Extractor):
    def extract_file(self, source_path: str, dest_path: str) -> bool:
        pass


    def supported_file(self) -> str | list[str]:
        """
        :returns: a string or list of strings of the file type which the extractor can use
        e.g. "gzip" or ["tar", "tarball"]
        """
        return SUPPORTED_FILE_TYPES