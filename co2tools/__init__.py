import sys
import os.path
from co2tools.mergers import merge
from co2tools.stl import solidify
from co2tools.__version__ import __version__
from yaml import load, SafeLoader


def help():
    print('co2tools [options] [action] [group]')
    print('Options:')
    print('\t--version\tPrint version')
    print('\t--base=folder\tSet base folder')
    print('Actions:')
    print('\tmerge\tRun only merge from yml file')
    print('\tsolidify\tRun only solidify from yml file')
    print('Group:')
    print('\tgpu\tDefines what group to run from yml file for given action')

def main():
    yaml_file = '.co2tools.yml'
    execute_action = None
    execute_section = None
    execute_file = None
    boolean_engine =  None
    base_folder = ''

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        i += 1
        if arg.lower() == '--version':
            print('co2tools v{}'.format(__version__))
            quit()
        if arg.lower() == '--yaml':
            yaml_file = sys.argv[i]
            i += 1
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
        if arg.lower() == '--engine':
            boolean_engine = sys.argv[i]
            i += 1
            continue
        if execute_action is None:
            execute_action = arg
            continue
        if execute_section is None:
            execute_section = arg
            continue
        if execute_file is None:
            execute_file = arg
            continue
        else:
            execute_file = '{} {}'.format(execute_file, arg)
            continue
        raise BaseException(1, 'Unknown command line argument!!!')

    if base_folder is not None:
        yaml_file = '{}{}'.format(base_folder, yaml_file)

    if not os.path.exists(yaml_file):
        raise BaseException(1, 'File \'{}\' does not exist!!!'.format(yaml_file))

    with open(yaml_file, 'r') as f:
        yaml_data = load(f, Loader=SafeLoader)

        if 'merge' in yaml_data:
            merge(yaml_data, execute_action, execute_section, execute_file, base_folder)

        if 'solidify' in yaml_data:
            solidify(yaml_data, execute_action, execute_section, execute_file, base_folder, boolean_engine)

        if 'macros' in yaml_data:
            pass

if __name__ == '__main__':
    main()
