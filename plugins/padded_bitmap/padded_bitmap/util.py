import struct


def find_padded_bytes(
        height: int,
        width: int,
        color_depth: int,
        total_image_size: int,
        header_size: int
        ) -> int:
    """
    :height: the number of vertical pixels
    :width: the number of horizontal pixels
    :color_depth: the number of bits representing the color of each pixel (should be a multiple of 8)
    :total_image_size: the actual size of the image (taken from the header!) in __bytes__
    :header_size: the size of the bitmap header in bytes
    :returns: the number of padded bytes
    """

    bytes_per_pixel = color_depth // 8 # covert the color depth (# of bits representing the color of the pixel) to bytes
    total_pixels = height * width  # find the number of pixels in the image
    expected_pixel_data_size = total_pixels * bytes_per_pixel # find the number of bytes of image data we're expecting
    padding = total_image_size - (expected_pixel_data_size + header_size) # subtract the known image size from the actual size

    return padding


def identify_padding(
        height: int,
        width: int,
        color_depth: int,
        total_image_size: int,
        header_size: int
        ) -> bool:
    """
    Returns true if there is obvious padding, returns false otherwise. Given
    a normal bitmap this function will never return a false positive, but
    may return false negatives for less obvious padding techniques
    :height: the number of vertical pixels
    :width: the number of horizontal pixels
    :color_depth: the number of bits representing the color of each pixel (should be a multiple of 8)
    :total_image_size: the actual size of the image (taken from the header!) in __bytes__
    :header_size: the size of the bitmap header in bytes
    :returns: true/false if padded
    """
    
    padding = find_padded_bytes(height, width, color_depth, total_image_size, header_size)

    # a positive value indicates superfluous bytes
    if padding > 0:
        return True
    else:
        return False


def get_padding_for_file(data: bytes) -> int | None:
    # source: https://en.wikipedia.org/wiki/BMP_file_format
    raw_header = data[0:14]
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
        dib_header = data[14:54]
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

        return find_padded_bytes(height, width, bits_per_pixel, image_size, 54)

    # FTODO: Something for a later day, these don't seem super common
    elif dib_type == 0x4142:
        raise NotImplementedError("OS/2 Bitmap formats are not currently supported")
    elif dib_type == 0x4943:
        raise NotImplementedError("OS/2 Bitmap formats are not currently supported")
    elif dib_type == 0x5043:
        raise NotImplementedError("OS/2 Bitmap formats are not currently supported")
    elif dib_type == 0x5440:
        raise NotImplementedError("OS/2 Bitmap formats are not currently supported")
    else:
        return None