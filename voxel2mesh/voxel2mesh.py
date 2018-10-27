import sys
import os
sys.path.append('../VoxelPopulating_Boolean')
sys.path.append('../marhing_cubes_for_voxels')

import map_loader
import voxel_operation
import boolean_operation
from marching_cubes_3d import *

TILE_NUMS   = 9
FRAME_NUM   = 1823
SIDE_LENGTH = 80
SOURCE_PATH = '../reactive_diffusion_network_java/output'

boxSpacing  = 10
max_value   = 256
z_range     = 16
z_offset    = 6

nums = [i for i in range(TILE_NUMS)]

def export(mesh, filename):

    data = []
    data.append('# mesh exported from voxel2mesh by jonas & yuta')

    for n in mesh.nodes:
        data.append('v {} {} {}'.format(n.x, n.y, n.z))

    data.append('g triangles')
    tris = [f for f in mesh.faces if len(f.nodes)==3]
    for f in tris:
        index_list = [str(n.id) for n in f.nodes]
        data.append('f '+' '.join(index_list))

    data.append("g quads")
    quads = [f for f in mesh.faces if len(f.nodes)==4]
    for f in quads:
        index_list = [str(n.id) for n in f.nodes]
        oudata.append('f '+' '.join(index_list))

    with open(filename, mode='w') as f:
        f.write('\n'.join(data))

if __name__ == '__main__':
    
    for (i, j) in zip([nums[-1]] + nums[:-1], nums):

        print('%d, %d' % (i, j))

        cells_a = map_loader.load_map('%s/%d/%d.csv' % (SOURCE_PATH, FRAME_NUM, i), max_value, SIDE_LENGTH)
        cells_b = map_loader.load_map('%s/%d/%d.csv' % (SOURCE_PATH, FRAME_NUM, j), max_value, SIDE_LENGTH)

        # generate voxels
        set_a, _ = voxel_operation.create_3d_array(cells=cells_a, side_length=SIDE_LENGTH, z_range=z_range, max_value=max_value, is_positive=False)
        set_b, _ = voxel_operation.create_3d_array(cells=cells_b, side_length=SIDE_LENGTH, z_range=z_range, max_value=max_value)

        # boolean operation
        boolean_set = boolean_operation.union(set_a, set_b, z_offset)

        x_len = len(boolean_set)
        y_len = len(boolean_set[0])
        z_len = len(boolean_set[0][0])

        # add outmost layers to the voxels
        data = []
        for x in range(x_len+2):
            data_yz = []
            for y in range(y_len+2):
                data_z = []
                for z in range(z_len+2):

                    v = 1

                    if x > 0 and x < x_len+1 and y > 0 and y < y_len+1 and z > 0 and z < z_len+1:
                        v = boolean_set[x-1][y-1][z-1]

                    data_z.append(v)
                data_yz.append(data_z)
            data.append(data_yz)

        x_len = len(data)
        y_len = len(data[0])
        z_len = len(data[0][0])
        xd = yd = zd = 1

        # generate mesh
        mesh = Mesh()
        for x in range(x_len-1):
            for y in range(y_len-1):
                for z in range(z_len-1):

                    v1 = data[x][y][z]
                    v2 = data[x + xd][y][z]
                    v3 = data[x + xd][y + yd][z]
                    v4 = data[x][y + yd][z]
                    v5 = data[x][y][z + zd]
                    v6 = data[x + xd][y][z + zd]
                    v7 = data[x + xd][y + yd][z + zd]
                    v8 = data[x][y + yd][z + zd]

                    distances = [v1, v2, v3, v4, v5, v6, v7, v8]

                    mc = marching_cubes_3d_single_cell(distances, x, y, z, 1)

                    mesh.add_faces(mc.faces)
                    for n in mc.nodes:
                        mesh.add_node(n)

        mesh.collect_nodes()

        export(mesh=mesh, filename='./%d_%d.obj' % (i, j))