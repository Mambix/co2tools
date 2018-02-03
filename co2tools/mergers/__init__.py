from co2tools.mergers.dxf import DXF


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
