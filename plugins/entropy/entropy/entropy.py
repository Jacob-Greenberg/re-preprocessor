from repr_api.informational import Information
from .config import SUPPORTED_FILE_TYPES
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import math

class EntropyInformation(Information):
    def show_info(self, file_path: str) -> None:
        print("Showing entropy information for file:", file_path)
        with open(file_path, "rb") as f:
            data = f.read()
            if not data:
                raise ValueError("File is empty, cannot compute entropy.")

            byte_frequencies = [0] * 256
            for byte in data:
                byte_frequencies[byte] += 1

            entropy = 0.0
            data_length = len(data)
            for freq in byte_frequencies:
                if freq > 0:
                    p = freq / data_length
                    entropy -= p * math.log2(p)


        

        fig, ax = plt.subplots(2,1, figsize=(10, 2))
        # TODO: this is supposed to be a histogram visualization, but it dont look good
        ax[0].hist(byte_frequencies, bins=range(256), color='blue', alpha=0.7)
        ax[0].set_title('Byte Value Distribution')
        ax[0].set_xlabel('Byte Value (0-255)')
        ax[0].set_ylabel('Frequency')




        # Shannon entropy visualization
        colors = ["white", "green", "red"] # white for empty file, green for low entropy, red for high entropy
        cmap = mcolors.LinearSegmentedColormap.from_list("entropy_cmap", colors)
        gradient = np.linspace(0, 1, 256).reshape(1, -1)

        ax[1].imshow(gradient, aspect='auto', cmap=cmap, extent=[0, 8, 0, 1], alpha=0.3)
        ax[1].axvspan(3.5, 5, color='green', alpha=0.15, label='English Text (3.5-5.0)') # english text is usually 3.5-5
        ax[1].axvspan(7.5, 8, color='red', alpha=0.15, label='Compressed/Encrypted (7.5-8.0)') # anything over 7.5 is usually compressed
        ax[1].axvline(entropy, color='black', linewidth=3, label=f'File Entropy: {entropy:.2f}')

        ax[1].set_xlim(0, 8)
        ax[1].set_ylim(0, 1)
        ax[1].set_yticks([]) # remove y ticks
        ax[1].set_xlabel('Bits per byte')
        ax[1].set_title('Shannon Entropy')

        ax[1].legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.tight_layout()
        plt.show()