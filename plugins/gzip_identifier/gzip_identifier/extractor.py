from repr_api.extractor import Extractor
from .config import SUPPORTED_FILE_TYPES
import gzip

class ExtractGZip(Extractor):
    def extract_file(self, source_path: str, dest_path: str) -> bool:
        try:
            with gzip.open(source_path, 'rb') as compressed_file:
                with open(dest_path, 'wb') as decompressed_file:
                    decompressed_file.write(compressed_file.read())

            return True
        except gzip.BadGzipFile:
            return False
    def supported_file(self) -> str | list[str]:
        """
        :returns: a string or list of strings of the file type which the extractor can use
        e.g. "gzip" or ["tar", "tarball"]
        """
        return SUPPORTED_FILE_TYPES