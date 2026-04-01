
from repr_api.identifier import Identifier
from .config import SUPPORTED_FILE_TYPES
import struct

class IdentifyTar(Identifier):
    def identify_file(self, file_path: str) -> tuple[float, list[str]]:
        try:
            with open(file_path, "rb") as f:
                f.seek(0, 2)
                file_size = f.tell()

                if file_size < 262:
                    return 0, SUPPORTED_FILE_TYPES
            
                f.seek(257)
                magic_bytes = f.read(5)

                if len(magic_bytes) != 5 or magic_bytes != b'ustar':
                    return 0, SUPPORTED_FILE_TYPES
            
                f.seek(148)
                checksum = f.read(8)
                if len(checksum) != 8:
                    return 0, SUPPORTED_FILE_TYPES

                return 1, SUPPORTED_FILE_TYPES
        
        except (IOError, OSError) as e:
            print(e)
            return 0, SUPPORTED_FILE_TYPES