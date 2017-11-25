import sys
from co2tools.mergers.dxf import DXF
from co2tools.stl.builder import Builder
from yaml import load


def merge(yaml_data, execute_action=None, execute_group=None):
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
            raise BaseException('ERROR', 'Missing section {} in YAML file!!!'.format(execute_section))
    for execute_group in groups:
        dxf_data = merge_data[execute_group]
        print(dxf_data)
        for target, yaml_data in dxf_data.items():
            md = DXF(target, source_folder=source_folder, target_folder=target_folder)
            md.merge_files(yaml_data)

def solidify(yaml_data, execute_action=None, execute_group=None):
    if execute_action is not None:
        if execute_action != 'solidify':
            return
    solid_data = yaml_data['solidify']
    print(solid_data)
    source_folder = solid_data.get('sourceDirectory', None)
    target_folder = solid_data.get('targetDirectory', None)
    groups = solid_data.get('groups', None)
    if groups is None:
        groups = ['default']
    else:
        solid_data = groups
    if execute_group is not None:
        if execute_group in groups:
            groups = [execute_group]
        else:
            raise BaseException('ERROR', 'Missing section {} in YAML file!!!'.format(execute_section))
    for execute_group in groups:
        print('Processing group: {}'.format(execute_group))
        dxf_data = solid_data[execute_group]
        for source, data in dxf_data.items():
            target = data.get('save', '{}.stl'.format(source[:-4]))
            modifications = data.get('modifications', None)
            if modifications is None:
                raise BaseException('ERROR', 'No \'modifications\' section in YAML file!!!')
            b = Builder(source, source_folder=source_folder, target_folder=target_folder)
            b.build(modifications, target)

def help():
    print('Help...')

if __name__ == "__main__":
    yaml_file = '../.co2tools.yml'
    execute_action = None
    execute_section = None

    if len(sys.argv) > 1:
        execute_action = sys.argv[1]
        if execute_action.lower() == 'help':
            help()
            quit()
    if len(sys.argv) > 2:
        execute_section = sys.argv[2]

    with open(yaml_file, 'r') as f:
        yaml_data = load(f)
        # print(yaml_data)

    source_folder = yaml_data.get('sourceDirectory', None)
    target_folder = yaml_data.get('targetDirectory', None)

    if 'merge' in yaml_data:
        merge(yaml_data, execute_action, execute_section)

    if 'solidify' in yaml_data:
        solidify(yaml_data, execute_action, execute_section)

    if 'macros' in yaml_data:
        pass
