
######################################## Import all dependencies #######################################################
import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np
from mne.filter import filter_data, resample
from scipy import signal
from scipy.signal import detrend, find_peaks
from scipy.signal import butter, iirnotch, lfilter




################################# Load ecg data #########################################################################
matfile = sio.loadmat('test_ecg.mat')
my_ecg = np.array(*matfile['ecg'])


                               ########## Preprocessing parts #########

################################# Resampling>Upsampling from 125 Hz to 200 Hz ##########################################
sf_original = 125  #Hz
sf_new= 200        #Hz
numberOfsample = round (len(my_ecg) * float (sf_new) / sf_original)
print(numberOfsample)
ecg_upsampling = signal.resample(my_ecg, numberOfsample)  #use scipy resample for upsampling
plt.figure(1)
#plt.plot(my_ecg, label='Original ECG signal')                        #Consider whole signal
plt.plot(my_ecg[int(0):int(1000)], label='Original ECG signal')     # considered 1000 samples for better visualization
#plt.plot(ecg_upsampling, label='ECG signal after upsampling')
plt.plot(ecg_upsampling[int(0):int(1000)], label='ECG signal after upsampling')

plt.xlabel('Samples')
plt.ylabel('Amplitude')
plt.legend()
plt.title(" Original Signal Vs Upsampling signal (1000 samples considered for better visualization)")
#plt.show()


############################# Filter design for high frequency noise and base line wandering ##########################


                          ####### savitzky golay low pass filter for high frequency noise #######

ecg_LPfilter = signal.savgol_filter(ecg_upsampling, 21, 5)     # window size 21, polynomial order 3, vary depend on the signal
plt.figure(2)
#plt.plot(ecg_upsampling, label='Upsampling ECG signal')       #consider whole signal
plt.plot(ecg_upsampling[int(0):int(1000)], label='Upsampling ECG signal')
#plt.plot(ecg_LPfilter, label='After removing high frequecy noise(Savitzky golay)')
plt.plot(ecg_LPfilter [int(0):int(1000)], label='After removing high frequecy noise(Savitzky golay)') #consider 1000samples
plt.xlabel('Samples')
plt.ylabel('Amplitude')
plt.legend()
plt.title(" 1000 samples considered for better visualization")
#plt.show()


                             ########## Alternatively design low pass filter #############

                ################## Low pass filter (butter worth) design for high freq noise############

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5*fs        #nyquist rate
    normal_cutoff = cutoff/nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False, output='ba')
    return b, a

def lowpass(data, fs, order=5):
        b, a = butter_lowpass(cutoff_low, fs, order=order)
        y = lfilter(b, a, data)
        return y

cutoff_low = 95
ecg_LPfilter = lowpass(ecg_upsampling, 200, 5)
plt.figure(3)
#plt.plot(ecg_upsampling, label='Upsampling ECG signal')
plt.plot(ecg_upsampling[int(0):int(1000)], label='Upsampling ECG signal')
#plt.plot(ecg_LPfilter, color='red', label='Filtered signal(low pass filter(Butterworth))')
plt.plot(ecg_LPfilter[int(0):int(1000)], color='red', label='Filtered signal(low pass filter(Butterworth))')
plt.xlabel('Samples')
plt.ylabel('Amplitude')
plt.legend()
plt.title(" 1000 samples considered for better visualization")
#plt.show()


               ################## Detrend for removing  baseline wandering ############################

ecg_derend= detrend(ecg_LPfilter) #scipy detrend command
plt.figure(4)
#plt.plot(ecg_upsampling, label='Upsampling ecg signal') #consider whole signal
plt.plot(ecg_upsampling[int(0):int(1000)], label='Upsampling ecg signal')    #consider 1000 samples
#plt.plot(ecg_derend, color= 'blue', label='Filtered signal(low pass filter and detrend)')
plt.plot(ecg_derend[int(0):int(1000)], color= 'blue', label='Filtered signal(low pass filter and detrend)')
plt.xlabel('Samples')
plt.ylabel('Amplitude')
plt.legend()
plt.title(" 1000 samples considered for better visualization")
#plt.show()



                              ########## Alternatively design high pass filter##################

                     ###### High pass filter (butter worth filter) design for base line wandering #############

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5*fs
    normal_cutoff = cutoff/nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False, output='ba')
    return b, a

def highpass(data, fs, order=5):
    b,a = butter_highpass(cutoff_high, fs, order=order)
    x = lfilter(b,a,data)
    return x

cutoff_high = 0.5     # define cutoff value (0,5 - 0,6 for high pass)
ecg_HPfilter = highpass(ecg_LPfilter, 200, 5)   #200 hz sampling frq, order=5
plt.figure(5)
#plt.plot(ecg_upsampling, label='Upsampling ECG signal')  #consider whole signal
plt.plot(ecg_upsampling[int(0):int(1000)], label='Upsampling ECG signal')  #consider 1000 samples
#plt.plot(ecg_HPfilter, color= 'red', label='Filtered signal(low and high pass filter(butterworth))')
plt.plot(ecg_HPfilter[int(0):int(1000)], color= 'red', label='Filtered signal(low and high pass filter(butterworth))')
plt.xlabel('Samples')
plt.ylabel('Amplitude')
plt.legend()
plt.title(" 1000 samples considered for better visualization")
#plt.show()




##################### ############ R-R peaks detection ########################################################
#rr, _ = find_peaks(ecg_HPfilter, distance=40, height=280)  # 2 peaks seperatio distance 40, 280 eight cover all peaks , For whole signal
rr, _ = find_peaks(ecg_HPfilter[int(0):int(1000)], distance=40, height=280)  # 2 peaks seperatio distance 40, 280 eight cover all peaks ,
plt.figure(6)
#plt.plot(ecg_HPfilter)    # consider whole signal
plt.plot(ecg_HPfilter[int(0):int(1000)])   #consider 1000 samples
#plt.plot(rr, ecg_HPfilter[rr], 'o')
plt.plot(rr, ecg_HPfilter[rr], 'o')
plt.title('R peaks detection (1000 samples considered for better visualization)')
plt.xlabel('Samples')
plt.ylabel('Amplitude')
plt.legend()
plt.show()