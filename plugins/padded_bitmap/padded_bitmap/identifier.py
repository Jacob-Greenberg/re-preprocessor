
from repr_api.identifier import Identifier
from .config import SUPPORTED_FILE_TYPES
import struct
from .util import identify_padding, get_padding_for_file

class IdentifyPaddedBitmap(Identifier):
    def identify_file(self, file_path: str) -> tuple[float, list[str]]:
        with open(file_path, "rb") as f:
            data = f.read()

            padding = get_padding_for_file(data)

            if  padding is not None and padding > 0:
                return 1.0, SUPPORTED_FILE_TYPES
            else:
                return 0.0, SUPPORTED_FILE_TYPES