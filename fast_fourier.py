from scipy.fft import fft, ifft, fftfreq
from matplotlib import pyplot as plt
import numpy as np
from net_cdf_variables import open_trace


'''#x = np.load('outfile_name.npy')

N = 600

# sample spacing

T = 1.0 / 800.0

x = np.linspace(0.0, N*T, N, endpoint=False)

y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x) + 0.2*np.sin(150.0 * 2.0*np.pi*x)
print(y)
#y = np.load('outfile_name.npy')

print(y)

yf = fft(y)

xf = fftfreq(N, T)[:N//2]

#plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
plt.plot(y)
#plt.plot(x)
#plt.plot(y)

plt.grid()

plt.show()'''

'-----------------------------------------------TEST SINUS WAVE-----------------------------------------'

'''Fs = 1000 #sampling freqency

t = np.arange(0,1,1/Fs) #time axis, contains a time for every sample

f = 20; #Frecquncy

x = np.sin(2*np.pi*f*t) + 0.5*np.sin(2*np.pi*40*t) + 5*np.sin(2*np.pi*5*t) + np.sin(2*np.pi*100*t)


print(x)

plt.subplot(4,1,1)
plt.plot(t, x); plt.title('Sinusiodial Signal')
plt.xlabel('Time(s)'); plt.ylabel('Amplitude')

n = np.size(t) #frecqyency axis
fr = (Fs/2) * np.linspace(0, 1, n/2) #frequency axis

X = fft(x)
X_m = (2/n)*abs(X[0:np.size(fr)])

plt.subplot(4,1,2)
plt.plot(fr, X_m); plt.title('Magnitude Spectrum')
plt.xlabel('Frequency(Hz)'); plt.ylabel('Magnitude')
plt.tight_layout()'''

'-----------------------------------------------TEST SINUS WAVE-----------------------------------------'

data_link = 'C:/06_forskningsprosjekter/VEMOP/data/sites/Heimdal/GPR/C_14012021/C_14012021.mira'

line = 0 #1
channel = 3 #12
trace = 20989 #9692
sys = 0

'''data_link = 'C:/06_forskningsprosjekter/VEMOP/data/sites/Heimdal/GPR/G_03052021/G_03052021.mira'
line = 1
channel = 12
trace = 9692
sys = 0'''


data_all = open_trace(data_link, line, channel, trace, sys)

data = data_all[0]
filename = data_all[1]

signal2 = data[:, trace]

np.save('trace_for_spectral_analysis.npy', signal2)

signal3 = np.load('trace_for_spectral_analysis.npy')

signal2_flat = signal3.flatten()

sampling_frequency2 = float(data_all[2])

timewindow = round(float(data_all[3])/1000, 7)

number_of_samples = int(data_all[4])

print(sampling_frequency2, timewindow)


'-------------------------------------------------GPR___________________________________________________'
#sampling_frequency = 7130.77002
samples_time = np.arange(0, timewindow, timewindow/number_of_samples)

print(samples_time.size)


#signal = np.load('outfile_name.npy')
signal = np.load('c:/06_forskningsprosjekter\VEMOP\data\sites\Heimdal\GPR\C_14012021\schlizi\channel_A000 avgtr.npy')

signal_flat = signal2_flat

freq_axis = np.size(samples_time) #frecqyency axis

freq = (sampling_frequency2//8) * np.linspace(0, 1, freq_axis//8) #frequency axis

signal_fft = fft(signal_flat)
signal_magnitude = (2/freq_axis)*abs(signal_fft[0:np.size(freq)])

signal_magnitude[0] = 0

plt.subplot(4,1,3)
plt.plot(samples_time, signal); plt.title('GPR Signal')
plt.xlabel('Time(ns)'); plt.ylabel('Amplitude')

plt.subplot(4,1,4)
plt.plot(freq, signal_magnitude); plt.title('Frequency Spectrum')
plt.xlabel('Frequency(MHz)'); plt.ylabel('Magnitude')


plt.show()