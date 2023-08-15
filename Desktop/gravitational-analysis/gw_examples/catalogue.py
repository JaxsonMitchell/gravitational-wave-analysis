"""
Runs through getting a gravitational wave from a catalogue.

This code uses pycbc, a repository for gravitational wave astronomy.
This code is following a tutorial on their website: 
http://pycbc.org/pycbc/latest/html/catalog.html
"""

import pycbc.catalog

# Loads the catalog of data from 
c = pycbc.catalog.Catalog(source='gwtc-2')

# Names of mergers in the catalog
print(c.names)

# Approximate GPS time of the mergers
print([c[m].time for m in c])


import matplotlib.pyplot as plt
import pycbc.catalog

c = pycbc.catalog.Catalog(source="gwtc-2")
mchirp, elow, ehigh = c.median1d('mchirp', return_errors=True)
spin = c.median1d('chi_eff')

plt.errorbar(mchirp, spin, xerr=[-elow, ehigh], fmt='o', markersize=7)
plt.xlabel('Chirp Mass')
plt.xscale('log')
plt.ylabel('Effective spin')
plt.show()