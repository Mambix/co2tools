import ezdxf
import os
import operator


class DXF:
    @staticmethod
    def add_layer(layer_name, dxf, src_dxf):
        if layer_name not in dxf.layers:
            lay = src_dxf.layers.get(layer_name)
            dxf.layers.new(name=lay.dxf.name, dxfattribs={'linetype': lay.dxf.linetype, 'color': lay.dxf.color})

    def __init__(self, dxf_file, ignore_layers=None, rename_layers=None, base_folder=None, source_folder=None, target_folder=None):
        self.__base_folder = None
        if base_folder is not None:
            self.__base_folder = base_folder
            if self.__base_folder[-1] != '/':
                self.__base_folder += '/'
        self.__source_folder = None
        if source_folder is not None:
            self.__source_folder = source_folder
        self.__target_folder = None
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
            t = '{}'.format(e.dxftype)
            e_lay = self.__rename_layers.get(e.dxf.layer, e.dxf.layer)
            if t[14:17] == 'Arc':
                self.add_layer(e_lay, dxf, src)
                c = tuple(map(operator.add, e.dxf.center, move))
                target_msp.add_arc(c, e.dxf.radius, e.dxf.start_angle, e.dxf.end_angle, dxfattribs={'layer': e_lay})
            elif t[14:20] == 'Circle':
                self.add_layer(e_lay, dxf, src)
                c = tuple(map(operator.add, e.dxf.center, move))
                target_msp.add_circle(c, e.dxf.radius, dxfattribs={'layer': e_lay})
            elif t[14:19] == 'Point':
                self.add_layer(e_lay, dxf, src)
                loc = tuple(map(operator.add, e.dxf.location, move))
                target_msp.add_point(loc, dxfattribs={'layer': e_lay})
            elif t[14:18] == 'Text':
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
            elif t[14:19] == 'MText':
                # print('MTEXT: {}'.format(e.get_text()))
                self.add_layer(e_lay, dxf, src)
                c = (e.dxf.insert[0] + move[0], e.dxf.insert[1] + move[1], e.dxf.insert[2])
                target_msp.add_mtext(e.get_text(), dxfattribs={
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
            elif t[14:18] == 'Line':
                self.add_layer(e_lay, dxf, src)
                start = tuple(map(operator.add, e.dxf.start, move))
                end = tuple(map(operator.add, e.dxf.end, move))
                target_msp.add_line(start, end, dxfattribs={'layer': e_lay})
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
            elif t[14:20] == 'LWPoly':
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
            elif t[14:20] == 'Spline':
                self.add_layer(e_lay, dxf, src)
                points = e.get_fit_points()
                new_points = []
                for p in points:
                    new_points.append((p[0] + move[0], p[1] + move[1], p[2]))
                spline = target_msp.add_spline(new_points, dxfattribs={
                    'layer': e_lay,
                    'flags': e.dxf.flags
                })

                points = e.get_control_points()
                new_points = []
                for p in points:
                    new_points.append((p[0] + move[0], p[1] + move[1], p[2]))
                spline.set_control_points(new_points)

                spline.set_knot_values(e.get_knot_values())
                spline.set_weights(e.get_weights())

                spline.closed = e.closed
            elif t[14:20] == 'Modern':
                # addLayer(e.dxf.layer, dxf, src)
                # target_msp.add_entity(e)
                # ignore = 1
                pass
            else:
                print(t[14:])
                print(e_lay)
                # target_msp.add_entity(e)
            # source_msp.unlink_entity(e)
            # target_msp.add_entity(e)
        dxf.saveas(self.__dxf_file)

    def merge_files(self, yaml_data):
        if isinstance(yaml_data, dict):
            for source, copies in yaml_data.items():
                if not isinstance(copies[0], list):
                    copies = [copies]
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
