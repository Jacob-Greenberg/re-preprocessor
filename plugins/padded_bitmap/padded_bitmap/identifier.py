
from repr_api.identifier import Identifier
from .config import SUPPORTED_FILE_TYPES
import struct
from .util import identify_padding

class IdentifyPaddedBitmap(Identifier):
    def identify_file(self, file_path: str) -> tuple[float, list[str]]:
        with open(file_path, "rb") as f:
            # source: https://en.wikipedia.org/wiki/BMP_file_format
            raw_header = f.read(14)
            header = struct.unpack_from('<HIHHI',raw_header)
            dib_type = header[0]
            """
            Device-Independent Bitmaps (DIB)
            BM : Windows 3.1x, 95, NT, etc.
            BA : OS/2 struct bitmap array
            CI : OS/2 struct color icon
            CP : OS/2 const color pointer
            IC : OS/2 const struct icon
            PT : OS/2 pointer
            """
            file_size = header[1]
            reserved_1 = header[2]
            reserved_2 = header[3]
            pixel_data_offset = header[4]

            if dib_type == 0x4D42: # 'BM'
                dib_header = f.read(40)
                dib_info = struct.unpack_from('<IIIHHIIIIII', dib_header)
                # not really sure what dib_info[0] is... seems to always be 40
                width = dib_info[1]
                height = dib_info[2]
                planes = dib_info[3]
                bits_per_pixel = dib_info[4]
                compression = dib_info[5]
                image_size = dib_info[6]
                x_pixels_per_meter = dib_info[7]
                y_pixels_per_meter = dib_info[8]
                total_colors = dib_info[9]
                important_colors = dib_info[10]

                has_padding = identify_padding(
                    height,
                    width,
                    bits_per_pixel,
                    image_size,
                    14 + 40 # header size + dib header size
                )
                if has_padding:
                    return 1.0, SUPPORTED_FILE_TYPES
                else:
                    return 0, SUPPORTED_FILE_TYPES
            
            elif dib_type == 0x4142:
                return 1.0, SUPPORTED_FILE_TYPES

            elif dib_type == 0x4943:
                return 1.0, SUPPORTED_FILE_TYPES
        
            elif dib_type == 0x5043:
                return 1.0, SUPPORTED_FILE_TYPES

            elif dib_type == 0x5440:
                return 1.0, SUPPORTED_FILE_TYPES

            else:
                return 0, SUPPORTED_FILE_TYPES