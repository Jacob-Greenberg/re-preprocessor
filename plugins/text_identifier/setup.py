from setuptools import setup, find_packages

setup(
    name='text_identifier',
    version='0.0.1',
    packages=find_packages(),
    install_requires=['python-magic'],
    entry_points={
        'repr-identifier': [
            'identify-text = text_identifier.identifier:IdentifyText'
        ],
        'repr-extractor': [
            'extract-text = text_identifier.extractor:ExtractText'
        ]
    }
)
