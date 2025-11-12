from setuptools import setup, find_packages

 

setup(

    name='gzip_identifier',

    version='0.0.1',

    packages=find_packages(),

    install_requires=[],
    entry_points = {
        'repr-identifier': [
            'identify-gzip = gzip_identifier.identifier:IdentifyGZip'
        ],
        'repr-extractor': [
            'extract-gzip =  gzip_identifier.extractor:ExtractGZip'
        ]
    }
)

