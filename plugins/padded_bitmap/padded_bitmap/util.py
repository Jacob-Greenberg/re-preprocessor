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
