from setuptools import setup, find_packages

 

setup(

    name='pcap-identifier',

    version='0.0.1',

    packages=find_packages(),

    install_requires=['pypcapkit', 'dpkt'],
    entry_points = {
        'repr-identifier': [
            'identify-pcap = pcap.identifier:IdentifyPCAP'
        ],
        'repr-extractor': [
            'extract-pcap =  pcap.extractor:ExtractPCAP'
        ]
    }
)

