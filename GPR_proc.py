import numpy as np
import matplotlib.pyplot as plt

def DC_shift(trace_collection):
    data = np.load(trace_collection)

    newdata_DC_shift = np.asmatrix(np.zeros(data.shape))

    for tr in range(0, data.shape[1]):
        mean10 = int(np.round(np.mean(data[:10, tr])))
        newdata_DC_shift[:, tr] = np.reshape(data[:, tr] - mean10, (512, 1))

    x1 = data[:, 0]
    x2 = data[:, 1]
    x3 = data[:, 2]
    x4 = data[:, 3]
    x5 = data[:, 4]
    y = range(512, 0, -1)

    plt.subplot(1, 2, 1)
    plt.plot(x1, y)
    plt.plot(x2, y)
    plt.plot(x3, y)
    plt.plot(x4, y)
    plt.plot(x5, y)

    x1_DC_aligned = newdata_DC_shift[:, 0]
    x2_DC_aligned = newdata_DC_shift[:, 1]
    x3_DC_aligned = newdata_DC_shift[:, 2]
    x4_DC_aligned = newdata_DC_shift[:, 3]
    x5_DC_aligned = newdata_DC_shift[:, 4]

    plt.subplot(1, 2, 2)
    plt.plot(x1_DC_aligned, y)
    plt.plot(x2_DC_aligned, y)
    plt.plot(x3_DC_aligned, y)
    plt.plot(x4_DC_aligned, y)
    plt.plot(x5_DC_aligned, y)

    plt.show()

    np.save('trace_collection.npy', newdata_DC_shift)

def timezero_adjust(trace_collection):
    data = np.load(trace_collection)

    maxlen = data.shape[0]
    newdata_timezero = np.asmatrix(np.zeros(data.shape))

    # Go through all traces to find maximum spike
    maxind = np.zeros(data.shape[1], dtype=int)

    for tr in range(0, data.shape[1]):
        maxind[tr] = int(np.argmax(data[:, tr]))

    # Find the mean spike point
    meanind = int(np.round(np.mean(maxind)))

    # Shift all traces. If max index is smaller than
    # mean index, then prepend zeros, otherwise append
    for tr in range(0, data.shape[1]):
        if meanind > maxind[tr]:
            differ = int(meanind - maxind[tr])
            newdata_timezero[:, tr] = np.reshape(np.concatenate([np.zeros((differ)), data[0:(maxlen - differ), tr]]),
                                                (512, 1))
        elif meanind <= maxind[tr]:
            differ = maxind[tr] - meanind
            # newdata_aligned = np.append(newdata_aligned, np.concatenate([data[differ:maxlen, tr], np.zeros((differ))]), axis=1)
            newdata_timezero[:, tr] = np.reshape(np.concatenate([data[differ:maxlen, tr], np.zeros((differ))]),
                                                (512, 1))

    x1 = data[:, 0]
    x2 = data[:, 1]
    x3 = data[:, 2]
    x4 = data[:, 3]
    x5 = data[:, 4]
    y = range(512, 0, -1)

    plt.subplot(1, 2, 1)
    plt.plot(x1, y)
    plt.plot(x2, y)
    plt.plot(x3, y)
    plt.plot(x4, y)
    plt.plot(x5, y)

    x1_timezero = newdata_timezero[:, 0]
    x2_timezero = newdata_timezero[:, 1]
    x3_timezero = newdata_timezero[:, 2]
    x4_timezero = newdata_timezero[:, 3]
    x5_timezero = newdata_timezero[:, 4]

    plt.subplot(1, 2, 2)
    plt.plot(x1_timezero, y)
    plt.plot(x2_timezero, y)
    plt.plot(x3_timezero, y)
    plt.plot(x4_timezero, y)
    plt.plot(x5_timezero, y)

    plt.show()

    np.save('trace_collection.npy', newdata_timezero)

def readMALA(file_name):
    '''
    Reads the MALA .rd3 data file and the .rad header. Can also be used
    to read .rd7 files but I'm not sure if they are really organized
    the same way.
    INPUT:
    file_name     data file name without the extension!
    OUTPUT:
    data          data matrix whose columns contain the traces
    info          dict with information from the header
    '''
    # First read header
    info = readGPRhdr(file_name + '.rad')
    try:
        filename = file_name + '.rd3'
        data = np.fromfile(filename, dtype=np.int16)
    except:
        # I'm not sure what the format of rd7 is. Just assuming it's the same
        filename = file_name + '.rd7'
        data = np.fromfile(filename, dtype=np.int16)

    nrows = int(len(data) / int(info['SAMPLES']))

    data = (np.asmatrix(data.reshape(nrows, int(info['SAMPLES'])))).transpose()

    return data, info

def readGPRhdr(filename):
    '''
    Reads the MALA header
    INPUT:
    filename      file name for header with .rad extension

    OUTPUT:
    info          dict with information from the header
    '''
    # Read in text file
    info = {}
    with open(filename) as f:
        for line in f:
            strsp = line.split(':')
            info[strsp[0]] = strsp[1].rstrip()
    return info

def alignTraces(data):
    '''
    Aligns the traces in the profile such that their maximum
    amplitudes align at the average two-way travel time of the
    maximum amplitudes
    INPUT:
    data       data matrix whose columns contain the traces
    OUTPUT:
    newdata    data matrix with aligned traces
    '''

    maxlen = data.shape[0]
    newdata = np.asmatrix(np.zeros(data.shape))
    # Go through all traces to find maximum spike
    maxind = np.zeros(data.shape[1], dtype=int)
    for tr in range(0, data.shape[1]):
        maxind[tr] = int(np.argmax(data[:, tr]))
        print(maxind[tr])
    # Find the mean spike point
    meanind = int(np.round(np.mean(maxind)))
    print(meanind)
    #meanind = 50
    # Shift all traces. If max index is smaller than
    # mean index, then prepend zeros, otherwise append
    for tr in range(0, data.shape[1]):
        if meanind > maxind[tr]:
            differ = int(meanind - maxind[tr])
            newdata[:, tr] = np.vstack([np.zeros((differ, 1)), data[0:(maxlen - differ), tr]])
        elif meanind < maxind[tr]:
            differ = maxind[tr] - meanind
            newdata[:, tr] = np.vstack([data[differ:maxlen, tr], np.zeros((differ, 1))])
        else:
            newdata[:, tr] = data[:, tr]
    return newdata

def DC_shift_2(data):
    newdata_DC_shift = np.asmatrix(np.zeros(data.shape))

    for tr in range(0, data.shape[1]):
        mean10 = int(np.round(np.mean(data[:10, tr])))
        newdata_DC_shift[:, tr] = np.reshape(data[:, tr] - mean10, (data.shape[0], 1))

    return newdata_DC_shift

def remMeanTrace(data, ntraces):
    data = np.asmatrix(data)
    tottraces = data.shape[1]
    # For ridiculous ntraces values, just remove the entire average
    if ntraces >= tottraces:
        newdata = data - np.matrix.mean(data, 1)
    else:
        newdata = np.asmatrix(np.zeros(data.shape))
        halfwid = int(np.ceil(ntraces / 2.0))

        # First few traces, that all have the same average
        avgtr = np.matrix.mean(data[:, 0:halfwid + 1], 1)
        newdata[:, 0:halfwid + 1] = data[:, 0:halfwid + 1] - avgtr

        # For each trace in the middle
        for tr in tqdm(range(halfwid, tottraces - halfwid + 1)):
            winstart = int(tr - halfwid)
            winend = int(tr + halfwid)
            avgtr = np.matrix.mean(data[:, winstart:winend + 1], 1)
            newdata[:, tr] = data[:, tr] - avgtr

        # Last few traces again have the same average
        avgtr = np.matrix.mean(data[:, tottraces - halfwid:tottraces + 1], 1)
        newdata[:, tottraces - halfwid:tottraces + 1] = data[:, tottraces - halfwid:tottraces + 1] - avgtr

    print('done with removing mean trace')
    return newdata

