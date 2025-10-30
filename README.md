# RE Preprocessor

### Overview
A modular program to aid in file identification and decompression for reverse engineering.

### Setting up a Development Environment

0. Clone the repo
1. In the root project directory, create a Python virtual environment with `python3 -m venv venv`
2. Using the virtual environment, install the required Python packages with `pip install -r requirements.txt`


## Plugins

### REPr API

Plugins can access REPr functionality through an API. This API contains abstract classes for plugins. The API can be installed like so:
1.  `cd ./api`
2. `pip install -e .`

### Developing a Plugin

1. Create a new folder in the `plugins/` directory
2. Create a `setup.py` script and configure it to your liking. REPr discovers plugins via entrypoints so be sure to expose your identifiers/extractors with them:
```python
entry_points = {
    'repr-identifier': [
        'identify-gzip = gzip_identifier.identifier:IdentifyGZip'
    ],
    'repr-extractor': [
        'extract-gzip =  gzip_identifier.extractor:ExtractGZip'
    ]
}
```
3. Run `pip install -e .` from the plugin's root directory. *Note: if you update setup.py you will need to run this command again* 
4. By installing the plugin this way you only have to create the package once. Anything using the plugin will now automatically use the latest changes

### Plugin Guidelines

- Plugins are distributed as Python packages. If your plugin relies on another plugin/package make sure the dependency is noted

### Creating a Plugin to Share

1. In the plugin's root directory use `python3 -m build`
2. Install the plugin's `.whl` from the `dist/*` directory created by the build process