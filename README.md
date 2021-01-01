# co2tools
[![Travis](https://img.shields.io/travis/Mambix/co2tools.svg)](https://travis-ci.org/Mambix/co2tools)
[![Coverage Status](https://coveralls.io/repos/github/Mambix/co2tools/badge.svg?branch=master)](https://coveralls.io/github/Mambix/co2tools?branch=master)
[![PyPI](https://img.shields.io/pypi/v/co2tools.svg)](https://pypi.python.org/pypi/co2tools)
Easily convert 2D DXF drawing into 3D models

# installation
```
pip3 install co2tools
```

# usage
In order to run this tool create a file `.co2tools.yml` in your project folder.
This file will contain instructions which co2tools tool will execute.
Then you can run the tool in your folder and it will use yml file to execute instructions:
```
co2tools
# only merge
co2tools merge
# only solidify
co2tools solidify
# specific group
co2tools solidify gpu
```

# .co2tools.yml structure
There are 2 use cases for this tool. First one is merging multiple 2D `DXF` files into a single file.
I personally use this method to join parts I draw in separate DXF files into a single DXF file that is ready
to be cut with CO2 laser cutter.
Second usage of this tool is to create solids from 2D parts in DXF files. Note that at the moment
this was intended to have one part drawn per DXF file.

## Merge
```yaml
merge:
  sourceDirectory: '../dxf/blocks'
  targetDirectory: '../dxf'
  default:
    6mm_plywood_cut_left_right.dxf:
      6mm_wood_cut_left.dxf: [-201.0, 0.0]
      6mm_wood_cut_right.dxf: [201.0, 0.0]
    6mm_plywood_cut_front_back.dxf:
      6mm_wood_cut_front.dxf: [207.0, 0.0]
      6mm_wood_cut_back.dxf: [-207.0, 0.0]
    6mm_plywood_cut_top_bottom.dxf:
      6mm_wood_cut_top.dxf: [-207.0, 205.0]
      6mm_wood_cut_bottom.dxf: [207.0, 205.0]
    6mm_plywood_cut_gpu.dxf:
      6mm_wood_cut_gpu_front.dxf: [0.0, -17.0]
      6mm_wood_cut_gpu_bottom.dxf:
        - [0.0, 61.0]
        - [0.0, 183.0]
      6mm_wood_cut_gpu_support.dxf: [[0.0, -31.0], [0.0, -81.0], [0.0, -109.0],[0.0, -159.0]]
      6mm_wood_cut_gpu_holder.dxf: [[-140.0, -63.0], [0.0, -63.0], [0.0, -141.0], [140.0, -63.0]]
      6mm_wood_cut_nut_holder.dxf: [[-110.0, -140.0], [-90.0, -140.0], [90.0, -140.0], [110.0, -140.0]]
      6mm_wood_cut_nut_cover.dxf: [[-190.0, -140.0], [-170.0, -140.0], [-150.0, -140.0], [-130.0, -140.0], [130.0, -140.0], [150.0, -140.0], [170.0, -140.0], [190.0, -140.0]]
```
Merge sections contains a couple of instructions we can pass to the library.
By default `sourceDirectory` and `targetDirectory` are set to current folder.
If needed you can override that by setting either relative or absolute path to your data.
I like to have DXF parts in subfolder `dxf/blocks` from where the parts are taken and the resulting
merged DXF if placed in `dxf` subfolder.
`default` section contains actual instructions needed for the library to combine parts.
First level that follows is the name of the destination dxf file.
This is the file that will contain merged data.
Next level provides the name of the source files. These are the files containing individual parts.
Values on the right describe what needs to be done to the data before it's added to the target file.
`[-201.0, 0.0]` instructs that the part is placed at X=-201.0 and Y=0.0 coordinates.
If you need to duplicate the part just define multiple target coordinates.

## Solidify
```yaml
solidify:
  sourceDirectory: '../dxf/blocks'
  targetDirectory: '../stl'
  groups:
    main:
      6mm_wood_cut_top.dxf:
        save: 'TOP.stl'
        modifications:
          - extrude: 6.0
          - translate: [.0, .0, 408.0]
      6mm_wood_cut_bottom.dxf:
        save: 'BOTTOM.stl'
        modifications:
          - extrude: 6.0
          - translate: [.0, .0, 47.0]
      6mm_wood_cut_left.dxf:
        save: 'LEFT.stl'
        modifications:
          - extrude: 6.0
          - rotate:
            - [math.pi/2, [1.0, 0.0, .0], [.0, .0, .0]]
            - [-math.pi/2, [.0, .0, 1.0], [.0, .0, .0]]
          - translate: [-200.0, .0, .0]
      6mm_wood_cut_right.dxf:
        save: 'RIGHT.stl'
        modifications:
          - extrude: 6.0
          - rotate:
            - [math.pi/2, [1.0, 0.0, .0], [.0, .0, .0]]
            - [math.pi/2, [.0, .0, 1.0], [.0, .0, .0]]
          - translate: [200.0, .0, .0]
      6mm_wood_cut_front.dxf:
        save: 'FRONT.stl'
        modifications:
          - extrude: 6.0
          - rotate:
            - [math.pi/2, [1.0, 0.0, .0], [.0, .0, .0]]
          - translate: [.0, 156.0, .0]
      6mm_wood_cut_back.dxf:
        save: 'BACK.stl'
        modifications:
          - extrude: 6.0
          - rotate: [math.pi/2, [1.0, 0.0, .0], [.0, .0, .0]]
          - translate: [.0, -180.0, .0]
    gpu:
      6mm_wood_cut_gpu_front.dxf:
        save: 'GPU_FRONT.stl'
        modifications:
          - extrude: 6.0
          - translate: [.0, -180.0, 281.0]
      6mm_wood_cut_gpu_bottom.dxf:
        save: 'GPU_BOTTOM.stl'
        modifications:
          - extrude: 6.0
          - translate: [.0, -73.0, 170.0]
      6mm_wood_cut_gpu_support.dxf:
        save: 'GPU_SUPPORT.stl'
        modifications:
          - extrude: 6.0
          - rotate: [-math.pi/2, [0.0, 0.0, 1.0], [.0, .0, .0]]
          - translate: [.0, -73.0, 170.0]
```
Solidify section provides instructions to create 3D STL files from 2D DXF information.
Just like with merge section `sourceDirectory` and `targetDirectory` are used to modify source folders.
Groups contain the name of the group. Next level tells the library what DXF file to use.
`save` is used to define target STL filename. `modifications` section instructs the library how
to solidify 2D object:
- extrude: This sets the height of the object in mm.
- translate: this is the origin point where the part will be placed in 3D space. 3 values represent X, Y and Z axis.
- rotate: as the name suggest this instructs the library how to rotate the part once it created 3D object. It has 3 components:
  - rotation angle
  - vectors representing axis of rotation
  - rotation origin point
