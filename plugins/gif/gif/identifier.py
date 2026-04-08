from repr_api.identifier import Identifier
from .config import SUPPORTED_FILE_TYPES


class IdentifyGIF(Identifier):
    def identify_file(self, file_path: str) -> tuple[float, list[str]]:
        with open(file_path, "rb") as f:
            raw_header = f.read(6)

            if raw_header != b'GIF87a' and raw_header != b'GIF89a': # `GIF87a` or `GIF89a`
                return 0, SUPPORTED_FILE_TYPES

            return 1, SUPPORTED_FILE_TYPES