from repr_api.extractor import Extractor
from .config import SUPPORTED_FILE_TYPES
import gzip
import os

class ExtractGZip(Extractor):
    def extract_file(self, source_path: str, dest_path: str) -> bool:
        try:
            with gzip.open(source_path, 'rb') as compressed_file:
                data = compressed_file.read()
                if not data:
                    return False

                with open(dest_path, 'wb') as decompressed_file:
                    decompressed_file.write(data)

            return os.path.exists(dest_path) and os.path.getsize(dest_path) > 0


        except Exception as e:
            print(e)
            return False

    def supported_file(self) -> str | list[str]:
        """
        :returns: a string or list of strings of the file type which the extractor can use
        e.g. "gzip" or ["tar", "tarball"]
        """
        return SUPPORTED_FILE_TYPES