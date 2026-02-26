from setuptools import setup, find_packages

setup(

    name='gif_identifier',

    version='0.0.1',

    packages=find_packages(),

    install_requires=[],
    entry_points = {
        'repr-identifier': [
            'identify-gif = gif.identifier:IdentifyGIF'
        ]
    }
)

