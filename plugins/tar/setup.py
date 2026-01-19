from setuptools import setup, find_packages

 

setup(

    name='gzip_identifier',

    version='0.0.1',

    packages=find_packages(),

    install_requires=[],
    entry_points = {
        'repr-identifier': [
            'identify-tar = tar.identifier:IdentifyTar'
        ],
        'repr-extractor': [
            'extract-tar =  tar.extractor:ExtractTar'
        ]
    }
)

