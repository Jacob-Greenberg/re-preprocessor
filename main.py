"""
main.py
"""
from plugin_discovery import PluginDiscovery
import argparse
from importlib import import_module

def attempt_identify(identifiers: dict,
                     in_file_path: str,
                     confidence_threshold: float = None,
                     type_hint: str | list[str] = None):
    """
    Attempts to identify a file by using the suite of identifiers
    :identifiers: a dictionary of available identifiers
    :in_file_path: the filepath to the file to identify
    :confidence_threshold: if an identifier is above this threshold
                           then stop trying and just return
    :type_hint: a string or list of strings with identifiers to try
                first, best used with confidence_threshold
    :returns: a dictionary = {"<identifier>": <confidence>,
                              "cool_file": 1.0}
    """
    confidence_values = {}

    if type_hint != None:
        pass # TODO
    else:
       for identifier_name, info in identifiers.items():
            try:
                print(identifier_name)
                identifier_class = getattr(import_module(info['module']), info['attribute'])()
                confidence, types = identifier_class.identify_file(in_file_path)
                confidence_values[identifier_name] = confidence, types

                if confidence_threshold is not None and confidence >= confidence_threshold:
                    break
            except Exception as e:
                print(f"Error during identification: {e}")
                input("Press Enter to acknowledge")
                confidence_values[identifier_name] = -1, [] # indicates an error state
                continue # proceed to next identifier

    return confidence_values

def attempt_extract(extractors: dict, confidence: dict, in_file_path: str, out_file_path: str) -> bool:
    highest_confidence = None
    for identifier, conf in confidence.items():
        if highest_confidence is None or conf[0] > highest_confidence[0]:
            highest_confidence = conf

    suspected_format = highest_confidence[1]

    for _, info in extractors.items():
        extractor_class = getattr(import_module(info['module']), info['attribute'])()
        
        if not extractor_class.is_supported(suspected_format):
            continue

        res = extractor_class.extract_file(in_file_path, out_file_path)
        return res

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
                    prog='RE Preprocessor',
                    description='Identifies/Extracts files for easier reverse engineering',
                    usage='%(prog)s -i|e [options]'
                    )
    parser.add_argument('-I', '--identify', action='store_true', help='Attempt to identify the type of a given file')
    parser.add_argument('-E', '--extract', action='store_true', help='Attempt to extract a given file after trying to identify it')
    parser.add_argument('-i', '--infile', dest='infile', help='The file to read', required=True)
    parser.add_argument('-o', '--outfile', help='The directory to place extracted files', required=False)
    args = parser.parse_args()
    

    discovery = PluginDiscovery()
    print(f"[...] Found {len(discovery.extractors)} extractors and {len(discovery.identifiers)} identifiers")

    if args.identify:
        print("Attempting to identify")

        confidence = attempt_identify(discovery.identifiers, args.infile)
        print(confidence)
    elif args.extract:
        confidence = attempt_identify(discovery.identifiers, args.infile)
        print("Attempting to extract")
        res = attempt_extract(discovery.extractors, confidence, args.infile, args.outfile)
        if res:
            print("Extraction succeeded")
        else:
            print("Extraction failed")

    
    # room for expansion with more modes

