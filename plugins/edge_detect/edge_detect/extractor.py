from repr_api.extractor import Extractor
from .config import SUPPORTED_FILE_TYPES

from PIL import Image, ImageFilter

class ExtractEdge(Extractor):
    def extract_file(self, source_path: str, dest_path: str) -> bool:
        try:
            image = Image.open(source_path)
            width, height = image.size
            #greyscale = image.convert("L") # later iterations might include different views
            rgb = image.convert("RGB")

            rgb_pixels= rgb.load()
            for y in range(height):
                for x in range(width):
                    r, g, b = rgb_pixels[x, y]
            
                    # Extract the lowest bit and scale it up to 255
                    r = (r & 1) * 255
                    g = (g & 1) * 255
                    b = (b & 1) * 255
            
                    rgb_pixels[x, y] = (r, g, b)
    
            rgb.show()
            rgb.save(dest_path)
            return True
        except Exception as e:
            print(e)
            return False

    def supported_file(self) -> str | list[str]:
        """
        :returns: a string or list of strings of the file type which the extractor can use
        e.g. "gzip" or ["tar", "tarball"]
        """
        return SUPPORTED_FILE_TYPES

        from PIL import Image

def reveal_lsb(image_path):
    img = Image.open(image_path).convert('RGB')
    pixels = img.load()
    width, height = img.size

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            # Extract the lowest bit and scale it up to 255 (black or white)
            r = (r & 1) * 255
            g = (g & 1) * 255
            b = (b & 1) * 255
            
            pixels[x, y] = (r, g, b)
    
    img.show()
    img.save("revealed_lsb.png")