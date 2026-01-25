from setuptools import setup, find_packages

setup(

    name='padded_bitmap',

    version='0.0.1',

    packages=find_packages(),

    install_requires=[],
    entry_points = {
        'repr-identifier': [
            'identify-padded-bitmap = padded_bitmap.identifier:IdentifyPaddedBitmap'
        ],
        'repr-extractor': [
            'extract-padded-bitmap  =  padded_bitmap.extractor:ExtractPaddedBitmap'
        ]
    }
)

