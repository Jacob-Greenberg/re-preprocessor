from repr_api.extractor import Extractor
from .config import SUPPORTED_FILE_TYPES
from .util import find_padded_bytes


class ExtractPaddedBitmap(Extractor):
    def extract_file(self, source_path: str, dest_path: str) -> bool:
        pass

        # TODO: identify where the padded bytes are and extract them to their own file


    def supported_file(self) -> str | list[str]:
        """
        :returns: a string or list of strings of the file type which the extractor can use
        e.g. "gzip" or ["tar", "tarball"]
        """
        return SUPPORTED_FILE_TYPES