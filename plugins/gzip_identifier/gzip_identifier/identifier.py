
from repr_api.identifier import Identifier
import gzip

class IdentifyGZip(Identifier):
    def identify_file(self, file_path: str) -> float:
        try:
            # TODO: the python gzip library is pretty forgiving when it comes
            # to opening things that aren't gzips. This should probably be a byte-level
            # header check
            gzip.open(file_path)
            return 1
        except gzip.BadGzipFile:
            return 0