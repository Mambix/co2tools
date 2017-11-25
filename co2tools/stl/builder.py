import trimesh
import numpy as np
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
        for layer in self.__layers:
            if layer == '0':
                continue
            E = copy.deepcopy(self.__dxf.entities[self.__dxf.metadata['layers'] == layer])
            path = trimesh.path.Path2D(entities=E, vertices=self.__dxf.vertices.copy())
            if extrude_height is None:
                elements[layer] = path
            else:
                extrude_by = extrude_height
                if layer == self.LAYER_HOLES:
                    extrude_by += 2.0
                extruded = path.extrude(extrude_by)
                if layer == self.LAYER_HOLES:
                    if isinstance(extruded, list):
                        for i in range(len(extruded)):
                            extruded[i].vertices -= [0.0, 0.0, 1.0]
                    else:
                        extruded.vertices -= [0.0, 0.0, 1.0]
                        extruded = [extruded]
                elements[layer] = extruded
        return elements

    def __init__(self, dxf_file):
        if not os.path.isfile(dxf_file):
            raise IOError("ERROR", "File not found!!!")
        self.__dxf_file = dxf_file
        try:
            self.__dxf = trimesh.load(self.__dxf_file)
            self.__layers = np.unique(self.__dxf.metadata['layers'])
        except ValueError as e:
            raise BaseException('{}: {}'.format(self.__dxf_file, e))
        self.LAYER_HOLES = 'HOLES'
        self.LAYER_CUT = 'CUT'
        self.ENGINE = 'blender'
        self.THREADS = 6
        self.stl = trimesh.load(self.__dxf_file)

    # def load_trimesh(self):
    #     self.stl = trimesh.load(self.__dxf_file)

    def extrude(self, extrude_height):
        dxf_elements = self.__dxf_elements(extrude_height)
        if dxf_elements is None:
            return
        print(dxf_elements.keys())
        self.stl = dxf_elements[self.LAYER_CUT]
        if 'IZREZ_PLEXI' in dxf_elements:
            if dxf_elements['IZREZ_PLEXI'] != []:
                self.stl = self.stl.difference(dxf_elements['IZREZ_PLEXI'], engine=self.ENGINE)
        if self.LAYER_HOLES in dxf_elements:
            holes_elements = dxf_elements[self.LAYER_HOLES]
            if not isinstance(dxf_elements, list):
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
                        # t.result.show()
                        holes_elements.append(t.result)
            # self.stl.show()
            # holes_elements[0].show()
            self.stl = self.stl.difference(holes_elements[0], engine=self.ENGINE)
        # self.stl.show()

    # def transform(self, transformations):
    #     for trans in transformations:
    #         self.stl.apply_transform(trans)

    def translate(self, matrix):
        self.stl.apply_transform(self.translation_matrix(matrix))

    def rotate(self, angle, direction, point=None):
        self.stl.apply_transform(self.rotation_matrix(angle, direction, point))

    def save(self, stl_file):
        if self.stl is None:
            raise BaseException("ERROR", "No STL data to save!!!")
        self.stl.export(stl_file)
