
from repr_api.identifier import Identifier
from .config import SUPPORTED_FILE_TYPES

from PIL import Image

class IdentifyEdge(Identifier):
    def identify_file(self, file_path: str) -> tuple[float, list[str]]:

        try:
            Image.open(file_path)
        except Exception as e:
            print(e)
            return 0, SUPPORTED_FILE_TYPES
        return 1, SUPPORTED_FILE_TYPES
