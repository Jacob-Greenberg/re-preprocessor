from repr_api.informational import Information
from .config import SUPPORTED_FILE_TYPES
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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

def calc_scanning_entropy(data: bytes, block_size: int) -> list[float]:
    entropy_data = []

    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        entropy_data.append(calc_shannon_entropy(block))

    return entropy_data

def byte_distribution(data: bytes) -> list[int]:
    distribution = [0] * 256

    for byte in data:
        distribution[byte] = distribution[byte] + 1
    
    return distribution

class EntropyInformation(Information):
    def show_info(self, file_path: str) -> None:
        print("Showing entropy information for file:", file_path)
        with open(file_path, "rb") as f:
            data = f.read()
            if not data:
                raise ValueError("File is empty, cannot compute entropy.")

            entropy = calc_shannon_entropy(data)
            entropy_data = calc_scanning_entropy(data, block_size = 1024)
            dist = byte_distribution(data)

        fig, (ax_block, ax_dist, ax_overall) = plt.subplots(3, 1, figsize=(10, 5), gridspec_kw={'height_ratios': [4, 4, 1]})
        plt.subplots_adjust(hspace=0.1)


        # Shannon entropy visualization
        colors = ["white", "green", "red"] # white for empty file, green for low entropy, red for high entropy
        cmap = mcolors.LinearSegmentedColormap.from_list("entropy_cmap", colors)
        gradient = np.linspace(0, 1, 256).reshape(1, -1)

        # entropy of 1k blocks
        ax_block.plot(range(len(entropy_data)),entropy_data)
        ax_block.set_title('Shannon Entropy per Block')
        ax_block.set_ylabel('Entropy (0-8)')
        ax_block.set_xlabel('Block #')
        ax_block.axhspan(3.5, 5.0, color='green', alpha=0.2, label='English Text')
        ax_block.axhspan(7.5, 8.0, color='red', alpha=0.2, label='Encrypted/Compressed')
        ax_block.grid(axis='y', linestyle='--', alpha=0.4)
        #ax_block.imshow(block_grad, aspect='auto', cmap=cmap, extent=[0, 1, 0, 8], alpha=0.3) # couldn't get this to work but it would look nice

        # byte distribution graph
        ax_dist.bar(range(256), dist)
        ax_dist.set_title('Byte Distribution')
        ax_dist.set_ylabel('Number of Occurrences')
        ax_dist.set_xlabel('Byte (0x0-0xff)')
        ax_dist.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'0x{int(x):02X}'))
        ax_dist.grid(axis='y', linestyle='--', alpha=0.4)

        # overall entropy
        ax_overall.imshow(gradient, aspect='auto', cmap=cmap, extent=[0, 8, 0, 1], alpha=0.3)
        ax_overall.axvspan(3.5, 5, color='green', alpha=0.15, label='English Text (3.5-5.0)') # english text is usually 3.5-5
        ax_overall.axvspan(7.5, 8, color='red', alpha=0.15, label='Compressed/Encrypted (7.5-8.0)') # anything over 7.5 is usually compressed
        ax_overall.axvline(entropy, color='black', linewidth=3, label=f'File Entropy: {entropy:.2f}')

        ax_overall.set_xlim(0, 8)
        ax_overall.set_ylim(0, 1)
        ax_overall.set_yticks([]) # remove y ticks
        ax_overall.set_title('Overall Shannon Entropy')
        ax_overall.legend(bbox_to_anchor=(1, 1))
        
        plt.tight_layout()
        plt.show()