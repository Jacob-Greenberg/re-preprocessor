from repr_api.informational import Information
from .config import SUPPORTED_FILE_TYPES
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import math

# Source for these two function: https://github.com/gchq/CyberChef/blob/master/src/core/operations/Entropy.mjs
def calc_shannon_entropy(data: bytes) -> float:
    prob = []
    occurrences = [0] * 256
    entropy = 0.0

    for byte in data:
        occurrences[byte] = occurrences[byte] + 1
        
    for occurrence in occurrences:
        if occurrence > 0:
            prob.append(occurrence / len(data))

    for p in prob:
        entropy = entropy + p * math.log2(p)

    return -entropy

def calc_scanning_entropy(data: bytes):
    entropy_data = []

    if len(data) < 256:
        bin_width = 8
    else:
        bin_width = 256

    for i in range(0, len(data), bin_width):
        block = data[i:i + bin_width]
        entropy_data.append(calc_shannon_entropy(block))
    print(len(entropy_data))
    return entropy_data, bin_width
    

class EntropyInformation(Information):
    def show_info(self, file_path: str) -> None:
        print("Showing entropy information for file:", file_path)
        with open(file_path, "rb") as f:
            data = f.read()
            if not data:
                raise ValueError("File is empty, cannot compute entropy.")

            entropy = calc_shannon_entropy(data)
            entropy_data, bin_width = calc_scanning_entropy(data)

        fig, (ax_hist, ax_bar) = plt.subplots(2, 1, figsize=(10, 5), gridspec_kw={'height_ratios': [4, 1]})
        plt.subplots_adjust(hspace=0.1)


        # TODO: this is supposed to be a histogram visualization, but it dont look good
        ax_hist.hist(entropy_data, bins=bin_width, color='#3498db', alpha=0.8)
        ax_hist.set_title('Byte Distribution & Shannon Entropy', fontsize=14, pad=15)
        ax_hist.set_ylabel('Byte Frequency')
        ax_hist.set_xlabel('Byte Value (0-255)')
        ax_hist.grid(axis='y', linestyle='--', alpha=0.4)
        ax_hist.set_xlim(0, bin_width)



        # Shannon entropy visualization
        colors = ["white", "green", "red"] # white for empty file, green for low entropy, red for high entropy
        cmap = mcolors.LinearSegmentedColormap.from_list("entropy_cmap", colors)
        gradient = np.linspace(0, 1, 256).reshape(1, -1)

        ax_bar.imshow(gradient, aspect='auto', cmap=cmap, extent=[0, 8, 0, 1], alpha=0.3)
        ax_bar.axvspan(3.5, 5, color='green', alpha=0.15, label='English Text (3.5-5.0)') # english text is usually 3.5-5
        ax_bar.axvspan(7.5, 8, color='red', alpha=0.15, label='Compressed/Encrypted (7.5-8.0)') # anything over 7.5 is usually compressed
        ax_bar.axvline(entropy, color='black', linewidth=3, label=f'File Entropy: {entropy:.2f}')

        ax_bar.set_xlim(0, 8)
        ax_bar.set_ylim(0, 1)
        ax_bar.set_yticks([]) # remove y ticks
        ax_bar.set_xlabel('Bits per byte')
        ax_bar.set_title('Shannon Entropy')
        ax_bar.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.tight_layout()
        plt.show()