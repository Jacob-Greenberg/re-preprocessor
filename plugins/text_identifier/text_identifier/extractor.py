from repr_api.extractor import Extractor
from .config import SUPPORTED_FILE_TYPES


class ExtractText(Extractor):
    def extract_file(self, source_path: str, dest_path: str) -> bool:
        # just a stub to make text file accept
        pass

    def supported_file(self) -> str | list[str]:
        return SUPPORTED_FILE_TYPES
