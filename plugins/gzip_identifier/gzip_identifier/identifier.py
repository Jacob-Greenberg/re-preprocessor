
from repr_api.identifier import Identifier
from .config import SUPPORTED_FILE_TYPES
import struct

class IdentifyGZip(Identifier):
    # source: https://en.wikipedia.org/wiki/Gzip
    def identify_file(self, file_path: str) -> tuple[float, list[str]]:
        with open(file_path, "rb") as f:
            raw_header = f.read(12)
            header = struct.unpack_from('<HccIcc',raw_header)
            
            magic_number = header[0]
            compression_method = header[1]
            flags = header[2]
            last_modified = header[3]
            extra_flags = header[4]
            compression_filesystem = header[5]

            # TODO: this should probably be a more sophisticated check
            if magic_number != 0x8B1F: # Match magic bytes
                return 0, SUPPORTED_FILE_TYPES

            return 1, SUPPORTED_FILE_TYPES