import os
import netCDF4 as nc
import xarray as xr
from matplotlib import pyplot as plt
import numpy as np

def define_NetCDF_variables(input_nc):
    working_directory = input_nc.rsplit('/', 1)[0]
    os.chdir(working_directory)
    nc_noExt = input_nc.rsplit('/', 1)[1].rsplit('.', 1)[0]
    NetCDF_GPR = nc_noExt + '.nc'

    nc_ds = nc.Dataset(NetCDF_GPR)
    xpixels = nc_ds.dimensions['x'].size
    ypixels = nc_ds.dimensions['y'].size
    zpixels = nc_ds.dimensions['z'].size

    dset = xr.open_dataset(NetCDF_GPR)
    gpr = dset.gpr

    x_temp = str(dset.gpr['x'][0])
    x_temp2 = x_temp.rsplit('\n')[1]
    x_coor = float(x_temp2.strip('array(').strip(')'))
    x_temp3 = str(dset.gpr['x'][1])
    x_temp4 = x_temp3.rsplit('\n')[1]
    x_coor2 = float(x_temp4.strip('array(').strip(')'))
    pixelsize = round(abs(x_coor - x_coor2), 2)

    y_temp = str(dset.gpr['y'][0])
    y_temp2 = y_temp.rsplit('\n')[1]
    y_coor = y_temp2.strip('array(').strip(')')

    return xpixels, ypixels, zpixels, pixelsize, y_coor, x_coor

def convert_NetCDF(vmin, vmax, filepath, depth):
    os.chdir(filepath.rsplit('/', 1)[0])
    nc_noExt = filepath.rsplit('/', 1)[1].rsplit('.', 1)[0]
    NetCDF_GPR = nc_noExt + '.nc'
    working_directory = filepath.rsplit('/', 1)[0]
    nc_ds = nc.Dataset(NetCDF_GPR)

    xpixels = nc_ds.dimensions['x'].size
    ypixels = nc_ds.dimensions['y'].size

    dset = xr.open_dataset(NetCDF_GPR)
    gpr = dset.gpr

    fig = plt.figure(figsize=(xpixels / 100, ypixels / 100))
    fig.figimage(gpr.isel(z=depth), cmap='Greys', origin='lower', vmin=vmin, vmax=vmax,
                            interpolation='bilinear', resample=False)

    try:
        os.chdir(working_directory)
        os.makedirs('NetCDF_img_%s' % nc_noExt)
        os.chdir(working_directory + '/NetCDF_img_%s' % nc_noExt)
    except FileExistsError:
        os.chdir(working_directory + '/NetCDF_img_%s' % nc_noExt)

    upper = '{0:0=4d}'.format(5 * depth)
    lower = '{0:0=4d}'.format(5 * depth + 5)

    newname = nc_noExt + "_" + upper + "_" + lower + '.jpg'
    plt.savefig(newname, quality=100)
    plt.close()


def find_nth(string, substring, n):
    if (n == 1):
        return string.find(substring)
    else:
        return string.find(substring, find_nth(string, substring, n - 1) + 1)

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

def open_trace(data_link, line, channel, trace, sys):

    print(sys)

    def readGPRhdr():
        info = {}
        with open(file_name + '.rad') as f:
            for line in f:
                strsp = line.split(':')
                info[strsp[0]] = strsp[1].rstrip()
        return info

    if sys == 0:
        if len(str(channel)) < 2:
            channel = 'A00' + str(channel)
        else:
            channel = 'A0' + str(channel)

        if len(str(line)) < 3:
            line = '0' * (3 - len(str(line))) + str(line)

        file_name = data_link[:-5] + '_' + line + '_' + channel

        info = readGPRhdr()
        filename = file_name + '.rd3'
        data = np.fromfile(filename, dtype=np.int16)
        nrows = int(len(data) / int(info['SAMPLES']))
        data = (np.asmatrix(data.reshape(nrows, int(info['SAMPLES'])))).transpose()
        sampling_frequency = info['FREQUENCY']
        timewindow = info['TIMEWINDOW']
        number_of_samples = info['SAMPLES']

        return data, filename, sampling_frequency, timewindow, number_of_samples


    elif sys == 1:
        channel = 0
        line_new = str(line).zfill(4)
        file_name = data_link[:-9] + '_' + line_new

        info = readGPRhdr()
        filename = file_name + '.rd3'
        data = np.fromfile(filename, dtype=np.int16)
        nrows = int(len(data) / int(info['SAMPLES']))
        data = (np.asmatrix(data.reshape(nrows, int(info['SAMPLES'])))).transpose()

        return data, filename



