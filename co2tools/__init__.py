import sys
import os.path
from co2tools.mergers import merge
from co2tools.stl import solidify
from __version__ import __version__
from yaml import load


def help():
    print('Help...')

def main():
    yaml_file = '.co2tools.yml'
    execute_action = None
    execute_section = None
    base_folder = ''

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        i += 1
        if arg.lower() == '--version':
            print('co2tools v{}'.format(__version__))
            quit()
        if arg[-4:].lower() == '.yml':
            yaml_file = arg
            continue
        if arg.lower() == 'help':
            help()
            quit()
        if arg.lower() == '--base':
            base_folder = sys.argv[i]
            if base_folder[-1] != '/':
                base_folder += '/'
            i += 1
            continue
        if execute_action is None:
            execute_action = arg
            continue
        if execute_section is None:
            execute_section = arg
            continue
        raise BaseException(1, 'Unknown command line argument!!!')

    if base_folder is not None:
        yaml_file = '{}{}'.format(base_folder, yaml_file)

    if not os.path.exists(yaml_file):
        raise BaseException(1, 'File \'{}\' does not exist!!!'.format(yaml_file))

    with open(yaml_file, 'r') as f:
        yaml_data = load(f)

        if 'merge' in yaml_data:
            merge(yaml_data, execute_action, execute_section, base_folder)

        if 'solidify' in yaml_data:
            solidify(yaml_data, execute_action, execute_section, base_folder)

        if 'macros' in yaml_data:
            pass

if __name__ == '__main__':
    main()
