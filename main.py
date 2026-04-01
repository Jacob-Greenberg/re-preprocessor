"""
main.py
"""
from plugin_discovery import PluginDiscovery
import argparse
from importlib import import_module
import os
from os import walk

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


def get_best_identification(confidence: dict):
    if not confidence:
        return 0.0, []
    best = max(confidence.items(), key=lambda kv: kv[1][0])
    return best[1]


def attempt_extract(extractors: dict, confidence: dict, in_file_path: str, out_file_path: str) -> bool:
    highest_score, suspected_format = get_best_identification(confidence)

    if highest_score <= 0 or not suspected_format:
        return False

    for _, info in extractors.items():
        extractor_class = getattr(import_module(info['module']), info['attribute'])()

        if not extractor_class.is_supported(suspected_format):
            continue

        try:
            return extractor_class.extract_file(in_file_path, out_file_path)
        except Exception as e:
            print(f"Error extracting {in_file_path} with {info['attribute']}: {e}")
            return False

    return False


def attempt_extract_for_recursive(extractors: dict, confidence: dict, in_file_path: str, output_root: str, depth: int) -> str | None:
    highest_score, suspected_format = get_best_identification(confidence)

    if highest_score <= 0 or not suspected_format:
        return None

    base = os.path.splitext(os.path.basename(in_file_path))[0]

    for _, info in extractors.items():
        extractor_class = getattr(import_module(info['module']), info['attribute'])()

        if not extractor_class.is_supported(suspected_format):
            continue

        outputs_directory = False
        if hasattr(extractor_class, 'outputs_directory'):
            try:
                outputs_directory = extractor_class.outputs_directory()
            except Exception as e:
                print(f"Warning: extractor {info['attribute']} outputs_directory() failed: {e}")

        if outputs_directory:
            target_path = os.path.join(output_root, f"{depth}_{base}")
            os.makedirs(target_path, exist_ok=True)
        else:
            target_path = os.path.join(output_root, f"{depth}_{base}.out")

        try:
            if extractor_class.extract_file(in_file_path, target_path):
                return target_path
        except Exception as e:
            print(f"Error extracting {in_file_path} with {info['attribute']}: {e}")
            return None

    return None


def check_information(informational_plugins: dict, in_file_path: str):
    plugin_references = []
    for i, (plugin_name, info) in enumerate(informational_plugins.items()):
        plugin_references.append(info)
        print(f"[{i + 1}] {plugin_name}")

    try:
        selection = int(input("Select an informational tool: ")) - 1
    except ValueError:
        print("[ ! ] Selection must be a number")
        quit(1)            
            
    try:
        info_class = getattr(import_module(plugin_references[selection]['module']), plugin_references[selection]['attribute'])()
    except IndexError:
        print("[ ! ] Invalid selection")
        quit(1)
            
    try:
        info_class.show_info(args.infile)
    except Exception as e:
        print(f"[ ! ] Encountered an error during plugin execution: {e}")
        quit(1)


def recursive_extract(discovery, source_file, output_root, max_depth=10):
    if not output_root:
        print("[ ! ] recursive_extract requires --outfile")
        return

    os.makedirs(output_root, exist_ok=True)

    queue = [(os.path.abspath(source_file), 0)]
    visited = set()

    while queue:
        current_file, depth = queue.pop(0)

        if depth > max_depth:
            print(f"[!] max recursion depth reached for {current_file}")
            continue

        if not os.path.exists(current_file):
            continue

        if os.path.isdir(current_file):
            for dirpath, _, filenames in os.walk(current_file):
                for filename in filenames:
                    queue.append((os.path.join(dirpath, filename), depth))
            continue

        if current_file in visited:
            continue
        visited.add(current_file)

        confidence = attempt_identify(discovery.identifiers, current_file)
        best_confidence, suspected_format = get_best_identification(confidence)
        print(f"[depth {depth}] {current_file} -> {best_confidence}, {suspected_format}")

        if best_confidence <= 0:
            continue

        target_path = attempt_extract_for_recursive(discovery.extractors, confidence, current_file, output_root, depth)
        print(f"Extract {current_file} -> {target_path} = {bool(target_path)}")

        if not target_path:
            continue

        if os.path.isdir(target_path):
            for dirpath, _, filenames in os.walk(target_path):
                for filename in filenames:
                    queue.append((os.path.join(dirpath, filename), depth + 1))
        elif os.path.isfile(target_path):
            queue.append((target_path, depth + 1))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
                    prog='RE Preprocessor',
                    description='Identifies/Extracts files for easier reverse engineering',
                    usage='%(prog)s -I|E [options]'
                    )
    parser.add_argument('-I', '--identify', action='store_true', help='Attempt to identify the type of a given file')
    parser.add_argument('-E', '--extract', action='store_true', help='Attempt to extract a given file after trying to identify it')
    parser.add_argument('-info', '--information', action='store_true', help='Attempt to show informational data about a given file')
    parser.add_argument('-i', '--infile', dest='infile', help='The file to read', required=True)
    parser.add_argument('-o', '--outfile', help='The directory to place extracted files', required=False)
    parser.add_argument('-r', '--recursive', action='store_true', help='Attempt to extract files recursively', required=False)
    args = parser.parse_args()
    

    discovery = PluginDiscovery()
    print(f"[...] Found {len(discovery.extractors)} extractors and {len(discovery.identifiers)} identifiers")

    if args.information:
        check_information(discovery.informational, args.infile)


    elif args.recursive and args.identify:
        print("Please use the -E/--extract flag in recursive mode")
        quit(code=1)

    elif args.identify:
        print("Attempting to identify")

        confidence = attempt_identify(discovery.identifiers, args.infile)

        print(confidence)
        for key, value in confidence.items():
            if value[0] > 0.5:
                break
        else:
            print("[ ? ] No high confidence identification")
            print("Additional information may be availible:")
            check_information(discovery.informational, args.infile)

    elif args.recursive and args.extract:
        if not args.outfile:
            print("[ ! ] Recursive extraction requires --outfile")
            quit(1)

        print(f"Starting recursive extraction: {args.infile} -> {args.outfile}")
        recursive_extract(discovery, args.infile, args.outfile, max_depth=20)

    elif args.extract:
        confidence = attempt_identify(discovery.identifiers, args.infile)
        print("Attempting to extract")
        res = attempt_extract(discovery.extractors, confidence, args.infile, args.outfile)
        if res:
            print("Extraction succeeded")
        else:
            print("Extraction failed")
            quit(1)

    
    # room for expansion with more modes

