from repr_api.identifier import Identifier
from .config import SUPPORTED_FILE_TYPES
import magic


class IdentifyText(Identifier):
    def identify_file(self, file_path: str) -> tuple[float, list[str]]:
        """Identify plain text files using python-magic."""
        try:
            mime_type = magic.from_file(file_path, mime=True)
        except Exception:
            return 0.0, SUPPORTED_FILE_TYPES

        # allow common MIME types to accept
        if mime_type is not None and (mime_type.startswith('text/') or mime_type in ('application/xml', 'application/json')):
            return 1.0, SUPPORTED_FILE_TYPES

        return 0.0, SUPPORTED_FILE_TYPES
