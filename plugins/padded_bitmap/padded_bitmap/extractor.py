from repr_api.extractor import Extractor
from .config import SUPPORTED_FILE_TYPES
from .util import find_padded_bytes, get_padding_for_file


class ExtractPaddedBitmap(Extractor):
    def extract_file(self, source_path: str, dest_path: str) -> bool:
        with open(source_path, 'rb') as f:
            data = f.read()
            padding = get_padding_for_file(data)

            if padding is None:
                raise TypeError("Unable to identify file")

            header_size = 14 + 40 # TODO: this is assumed for windows files but could be better

            padding_per_row = (len(data) - header_size) // padding
            
            # TODO: ugh, I need to know the bytes per row to find where the offset to the padding begins. I'm about to just make a bitmap library ATP





    def supported_file(self) -> str | list[str]:
        """
        :returns: a string or list of strings of the file type which the extractor can use
        e.g. "gzip" or ["tar", "tarball"]
        """
        return SUPPORTED_FILE_TYPES