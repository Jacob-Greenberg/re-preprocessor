from repr_api.extractor import Extractor
import gzip

class ExtractGZip(Extractor):
    def extract_file(self, source_path: str, dest_path: str) -> bool:
        print(f"Extracting from {source_path} to {dest_path}")
        return True
