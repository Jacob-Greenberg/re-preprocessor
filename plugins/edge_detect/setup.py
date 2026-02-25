from setuptools import setup, find_packages

 

setup(

    name='edge-detect',

    version='0.0.1',

    packages=find_packages(),

    install_requires=['pillow'],
    entry_points = {
        'repr-identifier': [
            'identify-edge = edge_detect.identifier:IdentifyEdge'
        ],
        'repr-extractor': [
            'extract-edge =  edge_detect.extractor:ExtractEdge'
        ]
    }
)

