from repr_api.extractor import Extractor
from .config import SUPPORTED_FILE_TYPES
import tarfile

class ExtractTar(Extractor):
    def extract_file(self, source_path: str, dest_path: str) -> bool:
        try:
            with tarfile.open(source_path, 'r') as tar_ref:
                tar_ref.extractall(dest_path)
            return True
        except Exception as e:
            print(f"Error extracting TAR file: {e}")
            return False

    def supported_file(self) -> str | list[str]:
        """
        :returns: a string or list of strings of the file type which the extractor can use
        e.g. "gzip" or ["tar", "tarball"]
        """
        return SUPPORTED_FILE_TYPES