import ezdxf
import os
import operator
import math
from ezdxf import math as dxfMath


class DXF:
    @staticmethod
    def add_layer(layer_name, dxf, src_dxf):
        if layer_name not in dxf.layers:
            lay = src_dxf.layers.get(layer_name)
            dxf.layers.new(name=lay.dxf.name, dxfattribs={'linetype': lay.dxf.linetype, 'color': lay.dxf.color})

    def __init__(self, dxf_file, ignore_layers=None, rename_layers=None, base_folder=None, source_folder=None, target_folder=None):
        self.__base_folder = ''
        if base_folder != '':
            self.__base_folder = base_folder
            if self.__base_folder[-1] != '/':
                self.__base_folder += '/'
        self.__source_folder = None
        if source_folder is not None:
            self.__source_folder = source_folder
        self.__target_folder = ''
        if target_folder is not None:
            self.__target_folder = target_folder
        self.__dxf_file = '{}{}/{}'.format(self.__base_folder, self.__target_folder, dxf_file)
        if os.path.isfile(self.__dxf_file):
            os.remove(self.__dxf_file)
        print('Target: {}'.format(self.__dxf_file))
        self.__ignore_layers = []
        if isinstance(ignore_layers, list):
            self.__ignore_layers = ignore_layers
        self.__rename_layers = {}
        if isinstance(rename_layers, dict):
            self.__rename_layers = rename_layers
        self.sum_perimeter = 0.0
        self.DEBUG = False

    def area(self, points):
        return 3.14

    def distance(self, start, end):
        if type(start) is tuple:
            return math.pow(math.pow(start[0]-end[0], 2) + math.pow(start[1]-end[1],2), 0.5)
        return math.pow(math.pow(start.x-end.x, 2) + math.pow(start.y-end.y,2), 0.5)

    def length(self, points):
        length = 0.0
        oldP = points[-1]
        for p in points:
            length += self.distance(oldP, p)
            oldP = p
        return length

    def merge(self, merge_dxf, move=(0.0, 0.0)):
        merge_dxf = '{}{}/{}'.format(self.__base_folder, self.__source_folder, merge_dxf)
        if not os.path.isfile(merge_dxf):
            raise IOError(2, 'No such file or directory: \'{}\''.format(merge_dxf))
        if not ezdxf.is_dxf_file(merge_dxf):
            raise IOError(2, 'No such file or directory: \'{}\''.format(merge_dxf))
        src = ezdxf.readfile(merge_dxf)

        print('\tAdding {}[{}] @ {}'.format(merge_dxf, src.dxfversion, move))
        dxf = ezdxf.new(src.dxfversion)
        lay = dxf.layers.get('0')
        lay.set_color(2)
        if os.path.isfile(self.__dxf_file):
            if ezdxf.is_dxf_file(self.__dxf_file):
                dxf = ezdxf.readfile(self.__dxf_file)
        target_msp = dxf.modelspace()
        source_msp = src.modelspace()

        # for lay in src.layers:
        for e in source_msp:
            if e.dxf.layer in self.__ignore_layers:
                continue
            e_lay = self.__rename_layers.get(e.dxf.layer, e.dxf.layer)
            if e.DXFTYPE == 'ARC':
                self.add_layer(e_lay, dxf, src)
                c = tuple(map(operator.add, e.dxf.center, move))
                target_msp.add_arc(c, e.dxf.radius, e.dxf.start_angle, e.dxf.end_angle, dxfattribs={'layer': e_lay})
                self.sum_perimeter += 2 * math.pi * e.dxf.radius * abs(e.dxf.start_angle-e.dxf.end_angle) / 360.0
            elif e.DXFTYPE == 'CIRCLE':
                self.add_layer(e_lay, dxf, src)
                c = tuple(map(operator.add, e.dxf.center, move))
                target_msp.add_circle(c, e.dxf.radius, dxfattribs={'layer': e_lay})
                self.sum_perimeter += 2 * math.pi * e.dxf.radius
            elif e.DXFTYPE == 'POINT':
                self.add_layer(e_lay, dxf, src)
                loc = tuple(map(operator.add, e.dxf.location, move))
                target_msp.add_point(loc, dxfattribs={'layer': e_lay})
            elif e.DXFTYPE == 'TEXT':
                self.add_layer(e_lay, dxf, src)
                c = (e.dxf.insert[0]+move[0], e.dxf.insert[1]+move[1], e.dxf.insert[2])
                target_msp.add_text(e.dxf.text, dxfattribs={
                    'insert': c,
                    'height': e.dxf.height,
                    'rotation': e.dxf.rotation,
                    'style': e.dxf.style,
                    'width': e.dxf.width,
                    'halign': e.dxf.halign,
                    'valign': e.dxf.valign,
                    'layer': e_lay
                })
            elif e.DXFTYPE == 'MTEXT':
                self.add_layer(e_lay, dxf, src)
                c = (e.dxf.insert[0] + move[0], e.dxf.insert[1] + move[1], e.dxf.insert[2])
                target_msp.add_mtext(e.text, dxfattribs={
                    'insert': c,
                    'char_height': e.dxf.char_height,
                    'width': e.dxf.width,
                    'attachment_point': e.dxf.attachment_point,
                    'flow_direction': e.dxf.flow_direction,
                    'style': e.dxf.style,
                    'rotation': e.dxf.rotation,
                    'line_spacing_style': e.dxf.line_spacing_style,
                    'line_spacing_factor': e.dxf.line_spacing_factor,
                    'layer': e_lay
                })
            elif e.DXFTYPE == 'LINE':
                self.add_layer(e_lay, dxf, src)
                start = tuple(map(operator.add, e.dxf.start, move))
                end = tuple(map(operator.add, e.dxf.end, move))
                target_msp.add_line(start, end, dxfattribs={'layer': e_lay})
                self.sum_perimeter += self.distance(e.dxf.start, e.dxf.end)
            # elif t[14:22] == 'Polyline':
            #     addLayer(e_lay, dxf, src)
            #     points = e.points()
            #     new_points = []
            #     for p in points:
            #         new_points.append((p[0] + move[0], p[1] + move[1]))
            #     poly = target_msp.add_polyline(new_points, dxfattribs={
            #         'layer': e_lay,
            #         'flags': e.dxf.flags
            #     })
            #     poly.closed = e.closed
            elif e.DXFTYPE == 'LWPOLYLINE':
                self.add_layer(e_lay, dxf, src)
                points = e.get_points()
                new_points = []
                for p in points:
                    new_points.append((p[0] + move[0], p[1] + move[1], p[2], p[3], p[4]))
                poly = target_msp.add_lwpolyline(new_points, dxfattribs={
                    'layer': e_lay,
                    'flags': e.dxf.flags
                })
                poly.closed = e.closed
                self.sum_perimeter += self.length(points)
            elif e.DXFTYPE == 'SPLINE':
                self.add_layer(e_lay, dxf, src)
                points = e.fit_points
                new_points = []
                for p in points:
                    new_points.append((p[0] + move[0], p[1] + move[1], p[2]))
                spline = target_msp.add_spline(new_points, dxfattribs={
                    'layer': e_lay,
                    'flags': e.dxf.flags
                })

                points = e.control_points
                new_points = []
                for p in points:
                    new_points.append((p[0] + move[0], p[1] + move[1], p[2]))
                spline.control_points = new_points

                spline.knots = e.knots
                spline.weights = e.weights

                spline.closed = e.closed
                self.sum_perimeter += self.length(points)
            elif e.DXFTYPE == 'MODERN':
                # addLayer(e.dxf.layer, dxf, src)
                # target_msp.add_entity(e)
                # ignore = 1
                pass
            else:
                if self.DEBUG:
                    print('Unhandled[{0}]: {1}'.format(e_lay, e.DXFTYPE))
                # target_msp.add_entity(e)
            # source_msp.unlink_entity(e)
            # target_msp.add_entity(e)
        dxf.saveas(self.__dxf_file)

    def merge_files(self, yaml_data):
        self.sum_perimeter = 0.0
        if isinstance(yaml_data, dict):
            for source, source_data in yaml_data.items():
                if isinstance(source_data, dict):
                    move = source_data.get('move', (0.0, 0.0))
                    if isinstance(move, list):
                        move = (move[0], move[1])
                    self.__ignore_layers = source_data.get('ignoreLayers', [])
                    self.__rename_layers = source_data.get('renameLayers', {})
                    self.merge(source, move=move)
                if isinstance(source_data, tuple):
                    self.merge(source, move=source_data)
                if isinstance(source_data, list):
                    if not isinstance(source_data[0], list):
                        copies = [source_data]
                    for copy in copies:
                        self.merge(source, move=(copy[0], copy[1]))
            return
        if isinstance(yaml_data, list):
            for source in yaml_data:
                for file, dic in source.items():
                    if isinstance(dic, dict):
                        move = (0.0, 0.0)
                        if 'move' in dic:
                            move = dic['move']
                        ignore_layers = self.__ignore_layers
                        rename_layers = self.__rename_layers
                        self.__ignore_layers = dic.get('ignoreLayers', ignore_layers)
                        self.__rename_layers = dic.get('renameLayers', rename_layers)
                        self.merge(file, move=move)
                        self.__ignore_layers = ignore_layers
                        self.__rename_layers = rename_layers
                    elif isinstance(dic, tuple):
                        self.merge(file, dic)
                    elif isinstance(dic, list):
                        for d in dic:
                            if isinstance(d, tuple):
                                self.merge(file, d)
                            else:
                                raise BaseException('ERROR', 'Instruction error!!!')
                    else:
                        raise BaseException('ERROR', 'Instruction error!!!')
            return
        raise BaseException("ERROR", "Unsupported format!!!")
