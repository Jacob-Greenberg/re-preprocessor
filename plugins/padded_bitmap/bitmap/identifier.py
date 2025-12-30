
from repr_api.identifier import Identifier
from .config import SUPPORTED_FILE_TYPES
import struct

class IdentifyPaddedBitmap(Identifier):
    def identify_file(self, file_path: str) -> tuple[float, list[str]]:
        with open(file_path, "rb") as f:
            raw_header = f.read(30)
            header = struct.unpack_from('<IHHHHHIIIHH',raw_header)
            
           
            # TODO: this should probably be a more sophisticated check
            if magic_number != 0x04034B50: # Match magic bytes
                return 0, SUPPORTED_FILE_TYPES

            return 1, SUPPORTED_FILE_TYPES