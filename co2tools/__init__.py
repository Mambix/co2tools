import sys
from co2tools.mergers.dxf import DXF
from co2tools.stl.builder import Builder
from yaml import load


def merge(yaml_data, execute_action=None, execute_group=None, base_folder=None):
    if execute_action is not None:
        if execute_action != 'merge':
            return
    merge_data = yaml_data['merge']
    source_folder = merge_data.get('sourceDirectory', None)
    target_folder = merge_data.get('targetDirectory', None)
    groups = merge_data.get('groups', None)
    if groups is None:
        groups = ['default']
    if execute_group is not None:
        if execute_group in groups:
            groups = [execute_group]
        else:
            raise BaseException('ERROR', 'Missing section {} in YAML file!!!'.format(execute_group))
    for execute_group in groups:
        dxf_data = merge_data[execute_group]
        print(dxf_data)
        for target, yaml_data in dxf_data.items():
            md = DXF(target, source_folder=source_folder, target_folder=target_folder, base_folder=base_folder)
            md.merge_files(yaml_data)

def solidify(yaml_data, execute_action=None, execute_group=None, base_folder=None):
    if execute_action is not None:
        if execute_action != 'solidify':
            return
    solid_data = yaml_data['solidify']
    print(solid_data)
    source_folder = solid_data.get('sourceDirectory', None)
    target_folder = solid_data.get('targetDirectory', None)
    layer_cut = solid_data.get('cutLayer', None)
    layer_holes = solid_data.get('holesLayer', None)
    layer_holes2 = solid_data.get('holesLayer2', None)
    groups = solid_data.get('groups', None)
    if groups is None:
        groups = ['default']
    else:
        solid_data = groups
    if execute_group is not None:
        if execute_group in groups:
            groups = [execute_group]
        else:
            raise BaseException('ERROR', 'Missing section {} in YAML file!!!'.format(execute_group))
    for execute_group in groups:
        print('Processing group: {}'.format(execute_group))
        dxf_data = solid_data[execute_group]
        for source, data in dxf_data.items():
            target = data.get('save', '{}.stl'.format(source[:-4]))
            modifications = data.get('modifications', None)
            if modifications is None:
                raise BaseException('ERROR', 'No \'modifications\' section in YAML file!!!')
            b = Builder(source, source_folder=source_folder, target_folder=target_folder, base_folder=base_folder)
            if layer_cut is not None:
                b.LAYER_CUT = layer_cut
            if layer_holes is not None:
                b.LAYER_HOLES = layer_holes
            if layer_holes2 is not None:
                b.LAYER_HOLES2 = layer_holes2
            b.build(modifications, target)

def help():
    print('Help...')

def main():
    yaml_file = '.co2tools.yml'
    execute_action = None
    execute_section = None
    base_folder = None

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        i += 1
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

    yaml_file = '{}{}'.format(base_folder, yaml_file)
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
