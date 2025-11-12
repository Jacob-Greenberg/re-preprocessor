
from repr_api.identifier import Identifier
from .config import SUPPORTED_FILE_TYPES

class IdentifyZIP(Identifier):
    def identify_file(self, file_path: str) -> tuple[float, list[str]]:
        pass