
from repr_api.identifier import Identifier
from .config import SUPPORTED_FILE_TYPES
import struct

class IdentifyTar(Identifier):
    def identify_file(self, file_path: str) -> tuple[float, list[str]]:
        # check for tar magic bytes at offset 257
        with open(file_path, "rb") as f:
            try:
                f.seek(257)
            except:
                return 0, SUPPORTED_FILE_TYPES
            raw_header = f.read(5)
            header = struct.unpack_from('5s',raw_header)
            
            magic_bytes = header[0]

            if magic_bytes != b'ustar': # Match magic bytes
                return 0, SUPPORTED_FILE_TYPES

            return 1, SUPPORTED_FILE_TYPES