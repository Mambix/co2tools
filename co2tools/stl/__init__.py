from co2tools.stl.builder import Builder


def solidify(yaml_data, execute_action=None, execute_group=None, execute_file=None, base_folder=None, engine=None):
    if execute_action is not None:
        if execute_action != 'solidify':
            return
    solid_data = yaml_data['solidify']
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
            if execute_file is not None:
                if execute_file != source:
                    continue
            target = data.get('save', '{}.stl'.format(source[:-4]))
            modifications = data.get('modifications', None)
            if modifications is None:
                raise BaseException('ERROR', 'No \'modifications\' section in YAML file!!!')
            b = Builder(source, source_folder=source_folder, target_folder=target_folder, base_folder=base_folder, options=yaml_data['solidify'])
            if layer_cut is not None:
                b.LAYER_CUT = layer_cut
            if layer_holes is not None:
                b.LAYER_HOLES = layer_holes
            if layer_holes2 is not None:
                b.LAYER_HOLES2 = layer_holes2
            if engine in ['blender', 'scad']:
                b.ENGINE = engine
            b.build(modifications, target)
