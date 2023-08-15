"""
Again this is another example obtained from pycbc's tutorials that I was following
Here is the link to the tutorial for a better explanation: 
http://pycbc.org/pycbc/latest/html/gw150914.html#plotting-the-whitened-strain
"""

import matplotlib.pyplot as plt
from pycbc.filter import highpass_fir, lowpass_fir
from pycbc.psd import welch, interpolate
from pycbc.catalog import Merger


for ifo in ['H1', 'L1']:
    """ For the information both in the
    Hanford and Livingston Detector. """
    h1 = Merger("GW150914").strain(ifo)
    h1 = highpass_fir(h1, 15, 8)

    # Calculating the noise spectrum. 
    psd = interpolate(welch(h1), 1 / h1.duration)

    # whiten
    white_strain = (h1.to_frequencyseries() / psd ** .5).to_timeseries()
    smooth = highpass_fir(white_strain, 35, 8)
    smooth = lowpass_fir(smooth, 300, 8)

    if ifo == 'L1':
        smooth *= -1
        smooth.roll(int(.007 / smooth.delta_t))

    plt.plot(smooth.sample_times, smooth, label=ifo)


plt.legend()
plt.xlim(1126259462.21, 1126259462.45)
plt.ylim(-150, 150)
plt.ylabel('Smoothed-Whitened Strain')
plt.grid()
plt.xlabel('GPS Time (s)')
plt.show()