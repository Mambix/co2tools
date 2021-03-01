from co2tools.mergers.dxf import DXF


def merge(yaml_data, execute_action=None, execute_group=None, execute_file=None, base_folder=None):
    if execute_action is not None:
        if execute_action != 'merge':
            return
    merge_data = yaml_data['merge']
    cutting_speed_per_time_unit = float(merge_data.get('cuttingSpeed', '900')) # 900mm/minute
    price_per_time_unit = float(merge_data.get('cuttingPrice', '0.5')) # 0.5EUR/minute
    cost_estimate_multiplier = float(merge_data.get('cuttingMultiply', '1.1')) # add 10% to the cost estimate
    source_folder = merge_data.get('sourceDirectory', None)
    target_folder = merge_data.get('targetDirectory', None)
    groups = merge_data.get('groups', None)
    if groups is None:
        groups = ['default']
    else:
        merge_data = groups
    if execute_group is not None:
        if execute_group in groups:
            groups = [execute_group]
        else:
            raise BaseException('ERROR', 'Missing section {} in YAML file!!!'.format(execute_group))
    for execute_group in groups:
        dxf_data = merge_data[execute_group]
        print(dxf_data)
        sum_perimeters = 0.0
        for target, yaml_data in dxf_data.items():
            if execute_file is not None:
                if execute_file != target:
                    continue
            md = DXF(target, source_folder=source_folder, target_folder=target_folder, base_folder=base_folder)
            md.merge_files(yaml_data)
            sum_perimeters += md.sum_perimeter
        print('Perimeter Sum: {:.3f}'.format(sum_perimeters))
        print('Estimated cost: {:.2f}{}'.format(cost_estimate_multiplier * price_per_time_unit * sum_perimeters / cutting_speed_per_time_unit, '€'))
