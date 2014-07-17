# Python standard library modules
import os
import sys

# 3rd party modules
import yaml


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..')

    # Load the general config
    try:
        config = yaml.load(open(os.path.join(config_path, 'config.yaml'), 'r'))
    except yaml.scanner.ScannerError:
        sys.stderr.write('Error: Could not parse config.yaml\n')
        sys.exit(1)
    except IOError:
        sys.stderr.write('Error: Could not open config.yaml\n')
        sys.exit(1)

    return config
