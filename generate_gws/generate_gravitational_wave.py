"""
A module on generating random waveforms of gravitational waves using 
the SEOBNRv4 approximant.
"""


from pycbc.waveform import get_td_waveform
from pycbc.detector import Detector
import matplotlib.pyplot as plt 
import random

class gravitationalWave:
    """ A class created for the analysis of gravitational waves. """
    def __init__(
            self,
            fs: int,
            mass1: float, 
            mass2: float, 
            spin1z: float = 0.0, 
            spin2z: float = 0.0, 
            inclination: float = 0.0, 
            coa_phase: float = 0.0,
            right_ascension: float = 0.0,
            declination: float = 0.0,
            polarization: float = 0.0,
        ):
        self.fs = fs
        self.mass1 = mass1
        self.mass2 = mass2
        self.spin1z = spin1z
        self.spin2z = spin2z
        self.inclination = inclination
        self.coa_phase = coa_phase
        hp, hc = gravitationalWave.buildWaveform(
            fs,
            mass1,
            mass2,
            spin1z,
            spin2z,
            inclination,
            coa_phase
        )
        self.hp = hp
        self.hc = hc

        self.right_ascension = right_ascension
        self.declination = declination
        self.polarization = polarization
    
    @classmethod
    def buildWaveform(
        self,
        fs: int,
        mass1: float, 
        mass2: float, 
        spin1z: float,
        spin2z: float,
        inclination: float, 
        coa_phase: float,
    ):
        """ Builds waveform of the gravitational wave. """
        hp, hc = get_td_waveform(
            approximant="SEOBNRv4",
            mass1=mass1,
            mass2=mass2,
            spin1z=spin1z,
            spin2z=spin2z,
            inclination=inclination,
            coa_phase=coa_phase,
            delta_t=1.0/fs,
            f_lower=40
        )
        return hp, hc
    
    def plotPolarizations(self) -> None:
        """ Plots hc and hp polarizations """
        plt.plot(self.hp.sample_times, self.hp, label="Plus Polarization")
        plt.plot(self.hc.sample_times, self.hc, label="Cross Polarization")
        plt.title(f"Merger of {round(self.mass1, 1)}M {round(self.mass2, 1)}M binary system.")
        plt.xlabel("Time")
        plt.ylabel("Strain")
        plt.show()

    def plotDetectors(self) -> None:
        """ Plots the gravitational wave as measured in the detectors """
        for detector in ['H1', 'L1', 'V1']:
            gw_measurement = (Detector(detector)).project_wave(
                self.hp, 
                self.hc,  
                self.right_ascension, 
                self.declination, 
                self.polarization
            )
            plt.plot(
                gw_measurement.sample_times, 
                gw_measurement,
                label=detector
            )
        plt.title(f"Merger of {round(self.mass1, 1)}M {round(self.mass2, 1)}M binary system.")
        plt.xlabel("Time")
        plt.ylabel("Strain")
        plt.show()

            


def randomGW(
    fs: int = 4096,
    mass_range: tuple = (5, 50),
    spin_range: tuple = (0,),
    inclination_range: tuple = (0,),
    coa_phase_range: tuple = (0,),
) -> gravitationalWave:
    """ Generates a random gravitational wave. """
    mass1 = getRandomValue(mass_range)
    mass2 = getRandomValue(mass_range)
    spin1z = getRandomValue(spin_range)
    spin2z = getRandomValue(spin_range)
    inclination = getRandomValue(inclination_range)
    coa_phase = getRandomValue(coa_phase_range)
    return gravitationalWave(
        fs, 
        mass1, 
        mass2, 
        spin1z, 
        spin2z, 
        inclination, 
        coa_phase
    )


def getRandomValue(bounds: tuple):
    """ Gets a random value from the tuple"""
    if len(bounds) == 1:
        return bounds[0]
    else:
        return random.uniform(
            bounds[0], 
            bounds[1]
        )

if __name__ == '__main__':
    gw = randomGW(mass_range=(8, 13))
    gw.plotPolarizations()
    gw.plotDetectors()

    