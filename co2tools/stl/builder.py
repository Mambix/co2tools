import trimesh
import numpy as np
import math
import copy
import threading
import os.path


class UnionThread(threading.Thread):
    def __init__(self, element1, element2):
        threading.Thread.__init__(self)
        self.element1 = element1
        self.element2 = element2
        self.result = None

    def run(self):
        self.result = self.element1.union(self.element2)


class Builder:
    @staticmethod
    def set_facets_color(stl, color):
        facets = stl.facets()
        for facet in facets:
            stl.visual.face_colors[facet] = color

    @staticmethod
    def rotation_matrix(angle, direction, point=None):
        return trimesh.transformations.rotation_matrix(angle, direction, point)

    @staticmethod
    def translation_matrix(matrix):
        return trimesh.transformations.translation_matrix(matrix)

    def __dxf_elements(self, extrude_height=None):
        elements = {}
        for layer in self.layers:
            if layer == '0':
                continue
            E = [x for x in self.dxf.entities if x.layer == layer]
            path = trimesh.path.Path2D(entities=E, vertices=self.dxf.vertices.copy())
            if extrude_height is None:
                elements[layer] = path
            else:
                extrude_by = extrude_height
                if layer in [self.LAYER_HOLES, self.LAYER_HOLES2]:
                    extrude_by += 1.0
                elements[layer] = path.extrude(extrude_by)
        return elements

    def __init__(self, dxf_file, source_folder='', target_folder='', base_folder='', options=None):
        self.LAYER_HOLES = 'HOLES'
        self.LAYER_HOLES2 = 'HOLES_PLEXI'
        self.LAYER_CUT = 'CUT'
        self.ENGINE = 'blender'
        self.THREADS = 16

        self.__base_folder = ''
        if base_folder != '':
            self.__base_folder = base_folder
            if self.__base_folder[-1] != '/':
                self.__base_folder += '/'
        self.__source_folder = ''
        if source_folder != '':
            self.__source_folder = source_folder
        self.__target_folder = None
        if target_folder is not None:
            self.__target_folder = target_folder
        self.__dxf_file = '{}{}/{}'.format(self.__base_folder, self.__source_folder, dxf_file)
        if not os.path.isfile(self.__dxf_file):
            raise IOError(2, 'No such file or directory: \'{}\''.format(self.__dxf_file))

        self.dxf = None
        self.layers = []
        self.stl = None

        try:
            print(self.__dxf_file)
            self.dxf = trimesh.load(self.__dxf_file, 'dxf')
            for layer in self.dxf.layers:
                if layer is not None and layer not in self.layers:
                    self.layers.append(layer)
        except ValueError as e:
            raise BaseException(e, '{}: {}'.format(self.__dxf_file, e))

        if options is not None:
            if 'LAYER_CUT' in options:
                self.LAYER_CUT = options['LAYER_CUT']
            if 'LAYER_HOLES' in options:
                self.LAYER_HOLES = options['LAYER_HOLES']
            if 'LAYER_HOLES2' in options:
                self.LAYER_HOLES2 = options['LAYER_HOLES2']

        print('    Source: {}'.format(self.__dxf_file))

    def extrude(self, extrude_height):
        dxf_elements = self.__dxf_elements(extrude_height)
        if dxf_elements is None:
            return
        print('        Layers: {}'.format(dxf_elements.keys()))
        if self.LAYER_CUT not in dxf_elements:
            raise BaseException(1, 'Layer {} is not present in DXF file.'.format(self.LAYER_CUT))
        self.stl = dxf_elements[self.LAYER_CUT]
        if isinstance(self.stl, list):
            raise BaseException("ERROR", "Empty STL object!!!")
            return
        if self.LAYER_HOLES2 in dxf_elements:
            holes_elements = dxf_elements[self.LAYER_HOLES2]
            if not isinstance(holes_elements, list):
                holes_elements = [holes_elements]
            while len(holes_elements)>1:
                holes_even = holes_elements[0::2]
                holes_odd = holes_elements[1::2]
                holes_elements = []

                if len(holes_even) > len(holes_odd):
                    holes_elements.append(holes_even[0])
                    del holes_even[0]

                while len(holes_odd) > 0:
                    threads = []
                    for i in range(len(holes_odd)):
                        ut = UnionThread(holes_even[-1], holes_odd[-1])
                        del holes_even[-1]
                        del holes_odd[-1]
                        ut.start()
                        threads.append(ut)
                        if len(threads) == self.THREADS:
                            break

                    for t in threads:
                        t.join()
                        holes_elements.append(t.result)
            holes_elements[0].apply_transform(self.translation_matrix([0.0, 0.0, -0.5]))
            diff_result = self.stl.difference(holes_elements[0], engine=self.ENGINE)
            # Workaround because it returns random results
            for i in range(5):
                tmp_result = self.stl.difference(holes_elements[0], engine=self.ENGINE)
                if tmp_result.mass > diff_result.mass:
                    diff_result = tmp_result
                    break
            self.stl = diff_result
        if self.LAYER_HOLES in dxf_elements:
            holes_elements = dxf_elements[self.LAYER_HOLES]
            if not isinstance(holes_elements, list):
                holes_elements = [holes_elements]
            while len(holes_elements)>1:
                holes_even = holes_elements[0::2]
                holes_odd = holes_elements[1::2]
                holes_elements = []

                if len(holes_even) > len(holes_odd):
                    holes_elements.append(holes_even[0])
                    del holes_even[0]

                while len(holes_odd) > 0:
                    threads = []
                    for i in range(len(holes_odd)):
                        ut = UnionThread(holes_even[-1], holes_odd[-1])
                        del holes_even[-1]
                        del holes_odd[-1]
                        ut.start()
                        threads.append(ut)
                        if len(threads) == self.THREADS:
                            break

                    for t in threads:
                        t.join()
                        holes_elements.append(t.result)
            holes_elements[0].apply_transform(self.translation_matrix([0.0, 0.0, -0.5]))
            diff_result = self.stl.difference(holes_elements[0], engine=self.ENGINE)
            # Workaround because it returns random results
            for i in range(5):
                tmp_result = self.stl.difference(holes_elements[0], engine=self.ENGINE)
                if tmp_result.mass > diff_result.mass:
                    diff_result = tmp_result
                    break
            self.stl = diff_result
        # self.stl.show()

    def translate(self, matrix):
        self.stl.apply_transform(self.translation_matrix(matrix))

    def rotate(self, instructions):
        if len(instructions) < 2:
            raise BaseException("ERROR", "Need at least 2 items in list for rotation!!!")
        angle, direction, point = eval(str(instructions[0]).lower()), instructions[1], None
        if len(instructions) > 2:
            point = instructions[2]
        self.stl.apply_transform(self.rotation_matrix(angle, direction, point))

    def save(self, stl_file):
        if self.stl is None:
            raise BaseException("ERROR", "No STL data to save!!!")
        stl_file = '{}{}/{}'.format(self.__base_folder, self.__target_folder, stl_file)
        print('        Saving: {}'.format(stl_file))
        self.stl.export(stl_file)

    def build(self, yaml_data, stl_file):
        for operations in yaml_data:
            for operation, instructions in operations.items():
                print('        {}: {}'.format(operation, instructions))
                if operation == 'extrude':
                    self.extrude(instructions)
                if operation == 'translate':
                    self.translate(instructions)
                if operation == 'rotate':
                    if isinstance(instructions[0], list):
                        for instruction in instructions:
                            self.rotate(instruction)
                    else:
                        self.rotate(instructions)
        self.save(stl_file)
