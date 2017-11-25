import math
from co2tools.mergers.dwg import Dwg
from co2tools.stl.builder import Builder
from yaml import load, dump
# try:
#     from yaml import CLoader as Loader, CDumper as Dumper
# except ImportError:
#     from yaml import Loader, Dumper


if __name__ == "__main__":
    yaml_file = '../.co2tools.yml'

    with open(yaml_file, 'r') as f:
        yaml_data = load(f)
        # print(yaml_data)

    if 'merge' in yaml_data:
        merge_data = yaml_data['merge']
        # print(merge_data)
        source_folder = merge_data.get('sourceDirectory', None)
        target_folder = merge_data.get('targetDirectory', None)
        if 'dwg' in merge_data:
            dwg_data = merge_data['dwg']
            print(dwg_data)
            for target, sources in dwg_data.items():
                md = Dwg(target, source_folder=source_folder, target_folder=target_folder)
                md.merge_files(sources)
    # md = Dwg('../dxf/6mm_plywood_cut_left_right.dxf')
    # md.merge_files([
    #     {'../dxf/blocks/6mm_wood_cut_left.dxf': (-201.0, 0.0)},
    #     {'../dxf/blocks/6mm_wood_cut_right.dxf': (201.0, 0.0)}
    # ])
    #
    # md = Dwg('../dxf/6mm_plywood_cut_front_back.dxf')
    # md.merge_files([
    #     {'../dxf/blocks/6mm_wood_cut_front.dxf': (207.0, 0.0)},
    #     {'../dxf/blocks/6mm_wood_cut_back.dxf': (-207.0, 0.0)}
    # ])
    #
    # md = Dwg('../dxf/6mm_plywood_cut_top_bottom.dxf')
    # md.merge_files([
    #     {'../dxf/blocks/6mm_wood_cut_top.dxf': (-207.0, 205.0)},
    #     {'../dxf/blocks/6mm_wood_cut_bottom.dxf': (207.0, 205.0)}
    # ])
    #
    # md = Dwg('../dxf/6mm_plywood_cut_gpu.dxf')
    # md.merge_files([
    #     {'../dxf/blocks/6mm_wood_cut_gpu_front.dxf': (0.0, -17.0)},
    #     {'../dxf/blocks/6mm_wood_cut_gpu_bottom.dxf': [(0.0, 61.0), (0.0, 183.0)]},
    #     {'../dxf/blocks/6mm_wood_cut_gpu_support.dxf': [(0.0, -31.0), (0.0, -81.0), (0.0, -109.0),(0.0, -159.0)]},
    #     {'../dxf/blocks/6mm_wood_cut_gpu_holder.dxf': [(-140.0, -63.0), (0.0, -63.0), (0.0, -141.0), (140.0, -63.0)]},
    #     {'../dxf/blocks/6mm_wood_cut_nut_holder.dxf': [(-110.0, -140.0), (-90.0, -140.0), (90.0, -140.0), (110.0, -140.0)]},
    #     {'../dxf/blocks/6mm_wood_cut_nut_cover.dxf': [(-190.0, -140.0), (-170.0, -140.0), (-150.0, -140.0), (-130.0, -140.0), (130.0, -140.0), (150.0, -140.0), (170.0, -140.0), (190.0, -140.0)]}
    # ])
    #
    # # Frame
    # b = Builder('6mm_wood_cut_top')
    # b.extrude(6.0)
    # b.translate((.0, .0, 407.0))
    # b.save('TOP.stl')
    #
    # b = Builder('6mm_wood_cut_bottom')
    # b.extrude(6.0)
    # b.translate((.0, .0, 47.0))
    # b.save('BOTTOM.stl')
    #
    # b = Builder('6mm_wood_cut_left')
    # b.extrude(6.0)
    # b.rotate(math.pi/2, (1.0, 0.0, .0), (.0, .0, .0))
    # b.rotate(-math.pi/2, (.0, .0, 1.0), (.0, .0, .0))
    # b.translate((-200.0, 0.0, .0))
    # b.save('LEFT.stl')
    #
    # b = Builder('6mm_wood_cut_right')
    # b.extrude(6.0)
    # b.rotate(math.pi/2, (1.0, 0.0, .0), (.0, .0, .0))
    # b.rotate(math.pi/2, (.0, .0, 1.0), (.0, .0, .0))
    # b.translate((200.0, 0.0, .0))
    # b.save('RIGHT.stl')
    #
    # b = Builder('6mm_wood_cut_front')
    # b.extrude(6.0)
    # b.rotate(math.pi / 2, (1.0, .0, .0), (.0, .0, .0))
    # b.translate((0.0, 156.0, .0))
    # b.save('FRONT.stl')
    #
    # b = Builder('6mm_wood_cut_back')
    # b.extrude(6.0)
    # b.rotate(math.pi / 2, (1.0, .0, .0), (.0, .0, .0))
    # b.translate((0.0, -180.0, .0))
    # b.save('BACK.stl')
    #
    # b = Builder('6mm_wood_cut_gpu_front')
    # b.extrude(6.0)
    # b.translate((0.0, -180.0, 281.0))
    # b.save('GPU_FRONT.stl')
    #
    # b = Builder('6mm_wood_cut_gpu_bottom')
    # b.extrude(6.0)
    # b.translate((0.0, -73.0, 170.0))
    # b.save('TOP.stl')
    #
    # b = Builder('6mm_wood_cut_gpu_support')
    # b.extrude(6.0)
    # b.rotate(-math.pi / 2, (.0, .0, 1.0), (.0, .0, .0))
    # b.save('GPU_SUPPORT.stl')
