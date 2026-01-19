from repr_api.extractor import Extractor
from .config import SUPPORTED_FILE_TYPES
import zipfile

class ExtractZIP(Extractor):
    def extract_file(self, source_path: str, dest_path: str) -> bool:
        try:
            with zipfile.ZipFile(source_path, 'r') as zip_ref:
                zip_ref.extractall(dest_path)
            return True
        except zipfile.BadZipFile:
            print("Error: Bad ZIP file.")
        except FileNotFoundError:
            print("Error: File not found.")
        except Exception as e:
            print(f"Unknown error extracting ZIP file: {e}")
        return False

    def supported_file(self) -> str | list[str]:
        """
        :returns: a string or list of strings of the file type which the extractor can use
        e.g. "gzip" or ["tar", "tarball"]
        """
        return SUPPORTED_FILE_TYPES