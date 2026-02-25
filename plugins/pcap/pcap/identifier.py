
from repr_api.identifier import Identifier
from .config import SUPPORTED_FILE_TYPES
from pcapkit import extract, HTTP, TCP, UDP
import struct

class IdentifyPCAP(Identifier):
    def identify_file(self, file_path: str) -> tuple[float, list[str]]:
        try:
            extract(fin=file_path, verbose=False, nofile=True)
        except:
            return 0, SUPPORTED_FILE_TYPES
        return 1, SUPPORTED_FILE_TYPES
