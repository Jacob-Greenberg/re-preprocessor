from repr_api.extractor import Extractor
from .config import SUPPORTED_FILE_TYPES
from gift import Gif


class ExtractGIFT(Extractor):
    def extract_file(self, source_path: str, dest_path: str) -> bool:
        try:
            with open(source_path, "rb") as f:
                gif = Gif(f, recover=True) # going to assume the user doesn't know the password

            with open(dest_path, 'wb+') as f:
                for blob in gif.blobs:
                    f.write(blob)

            return True
        except Exception as e:
            print(f"Error extracting data from GIF: {e}")
            return False

    def supported_file(self) -> str | list[str]:
        """
        :returns: a string or list of strings of the file type which the extractor can use
        e.g. "gzip" or ["tar", "tarball"]
        """
        return SUPPORTED_FILE_TYPES