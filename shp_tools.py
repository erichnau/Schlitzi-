import numpy as np
from fiona import collection
from scipy.spatial import KDTree
import pickle
import timeit

#datasource = 'C:/06_forskningsprosjekter/VEMOP/data/sites/Heimdal/GPR/A_23092020_A_sep2020_Antenna_Points.shp'
#ttt = 'C:/06_forskningsprosjekter/VEMOP/data/sites/Heimdal/GPR/G_03052021_G_mai2021_Antenna_Points.shp'
#datasource2 = 'C:/000_VEMOP_convert/nc/GPR/temp/C_14012021_C_jan2021_Antenna_Points.npy'

def shp_to_np_kdtree(datasource):
    with collection(datasource, "r") as source:
        features = list(source)

    line_nr = np.asarray([feat['properties']['Line'] for feat in features])
    ch_nr = np.asarray([feat['properties']['Channel'] for feat in features])
    pnt_nr = np.asarray([feat['properties']['Point'] for feat in features])
    coords = np.asarray([feat['geometry']['coordinates'] for feat in features])
    pts2D = np.delete(coords, np.s_[2::3], axis=1)
    tree = KDTree(pts2D)
    np_all = np.dstack((np.vstack((line_nr, ch_nr, pnt_nr)).T, coords))

    path = datasource[:datasource.rfind('/')+1]
    filename = ((datasource[datasource.rfind('/') + 1 :]).rsplit('.'))[0]
    newfile_np = path + filename +'.npy'
    newfile_kd = path + filename +'.pickle'

    np.save(newfile_np, np_all)

    with open(newfile_kd, 'wb') as f:
        pickle.dump(tree, f)


def nn_from_file(input_data, x, y, n):
    with open(input_data, 'rb') as f:
        tree = pickle.load(f)

        querypoint = np.asarray([[x, y]]),
        result = tree.query(querypoint, n)
        dist = []
        indices = []
        if n > 1:
            for i in range(n):
                dist.append(round(result[0][0][0][i], 3))
                indices.append(result[1][0][0][i])

        elif n == 1:
            dist.append(round(result[0][0][0], 3))
            indices.append(result[1][0][0])
        print(indices)

        return dist, indices

def kd_int_to_point_info(datasource, indices):
    points_np = np.load(datasource)
    point_IDs = []
    for i, index in enumerate(indices):
        line = int(points_np[index][0][0])
        channel = int(points_np[index][1][0])
        trace = int(points_np[index][2][0])

        point_info =[line, channel, trace]
        point_IDs.append(point_info)
        #point_IDs.append(channel)
        #point_IDs.append(trace)

    return point_IDs



#print(timeit.Timer(nn_from_file).timeit(number=1))
#print(timeit.Timer(kd_int_to_point_info).timeit(number=1))
#print(timeit.Timer(shp_to_np_kdtree).timeit(number=1))

#print(kd_int_to_point_info())