from repr_api.identifier import Identifier
from .config import SUPPORTED_FILE_TYPES
import struct

class IdentifyZIP(Identifier):
    # source: https://en.wikipedia.org/wiki/ZIP_(file_format)
    def identify_file(self, file_path: str) -> tuple[float, list[str]]:
        with open(file_path, "rb") as f:
            raw_header = f.read(30)
            header = struct.unpack_from('<IHHHHHIIIHH',raw_header)
            
            magic_number = header[0]
            version = header[1]
            flags = header[2]
            compression_method = header[3]
            last_modified_time = header[4]
            last_modified_date = header[5]
            crc = header[6]
            compressed_size = header[7]
            uncompressed_size = header[8]
            name_length = header[9]
            extra_length = header[10]
            # TODO: file name/extra field

            # TODO: this should probably be a more sophisticated check
            if magic_number != 0x04034B50: # Match magic bytes
                return 0, SUPPORTED_FILE_TYPES

            return 1, SUPPORTED_FILE_TYPES