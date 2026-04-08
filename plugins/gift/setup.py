from setuptools import setup, find_packages

setup(

    name='gift_extractor',

    version='0.0.1',

    packages=find_packages(),

    install_requires=['gift-stego'],
    entry_points = {
        'repr-extractor': [
            'extract-gift =  gift.extractor:ExtractGIFT'
        ]
    }
)

