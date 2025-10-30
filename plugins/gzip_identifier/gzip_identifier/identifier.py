
from repr_api.identifier import Identifier
from .config import SUPPORTED_FILE_TYPES
import gzip

class IdentifyGZip(Identifier):
    def identify_file(self, file_path: str) -> tuple[float, list[str]]:
        try:
            # TODO: the python gzip library is pretty forgiving when it comes
            # to opening things that aren't gzips. This should probably be a byte-level
            # header check
            gzip.open(file_path).close()
            return 1, SUPPORTED_FILE_TYPES
        except gzip.BadGzipFile:
            return 0, SUPPORTED_FILE_TYPES