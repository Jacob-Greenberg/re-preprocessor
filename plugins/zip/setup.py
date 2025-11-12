from setuptools import setup, find_packages

 

setup(

    name='zip_identifier',

    version='0.0.1',

    packages=find_packages(),

    install_requires=[],
    entry_points = {
        'repr-identifier': [
            'identify-zip = zip_identifier.identifier:IdentifyZIP'
        ],
        'repr-extractor': [
            'extract-zip =  zip_identifier.extractor:ExtractZIP'
        ]
    }
)

