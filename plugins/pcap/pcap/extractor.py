from repr_api.extractor import Extractor
from .config import SUPPORTED_FILE_TYPES
from pcapkit import extract, HTTP, TCP, UDP, FTP
import tarfile

class ExtractPCAP(Extractor):
    def extract_file(self, source_path: str, dest_path: str) -> bool:
        try:
            ext = extract(
                fin=source_path,
                store=False,
                nofile=True,
                reassembly=True,
                tcp=True
                )
            print("here")
            counter = 0
            for datagram in ext.reassembly.tcp:
                
                counter = counter + 1
                index = datagram.index
                src_ip = datagram.id.src[0]
                src_port = datagram.id.src[1]
                dst_ip =  datagram.id.dst[0]
                dst_port =  datagram.id.dst[1]
                header = datagram.header
                payload = datagram.payload
                with open(f"{dest_path}/{index[0]}-{index[-1]}", "wb") as f:
                    if isinstance(payload, bytes):
                        f.write(payload)
                    else:
                        f.write(b''.join(payload))


                #print(f"{src_ip}:{src_port} -> {dst_ip}:{dst_port}")
                #print(f"{src_ip}:{src_port} -> {dst_ip}:{dst_port} | {payload}")
                print(datagram)
                #print(f"{counter}************************************************")
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