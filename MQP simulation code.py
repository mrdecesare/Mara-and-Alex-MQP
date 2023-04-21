# Libraries needed
import numpy as np
import random 
import matplotlib.pyplot as plt


# random values for each of the variables we control for the expirament 
# the min and max values are set according to the system in the lab
amp = np.random.uniform(0, 10) # in volts bc thats what our output is in real life 
fre = random.randint(183000, 185000)# in MHz, cannot do GHz because wont work
fre_start = fre - 10
fre_end = fre + 10
fre_range = np.linspace(fre_start, fre_end, 50000) # we want the sweep to be 20 MHz thats this does
pres = random.randint(1, 200) # safe range to complete the expirament in Torr 
    # because this function doesnt allow you to go smaller then 1 
    # if we say the values are in mTorr then the curve is way too wide
#mod_steps = random.randint(1,2000) # choosing a random number of modulation steps
# note: 1 step = a 20MHz sweep and 2000 steps = 1 kHz/sweep

def Gaussian(amp, fre, pres): 
    x = fre_range # simplifies the variable for the frequency range equation just for the function
    g = -amp*np.exp(-(x-fre)**2/(2*(pres/1000)**2)) # eq for gaussian curve 
    # x-fre--> position of the center of the gaussian curve
    # pres/1000 --> converts the pressure into mTorr for more accurate gaussian curve
    return(g)


nu_mod_range = (0.01,20) # modulated frequncy range in MHz (numbers the same reason for mod_steps)
delta = (0.1,100) # modulated amplitude range (just doing the same as amp)
nu_mod = np.random.uniform(nu_mod_range[0], nu_mod_range[1]) #modulated frequncy

Gaussian_Mod = Gaussian(amp, fre, pres) * np.sin(2 * np.pi * nu_mod *fre_range)
# eq for sin modulated Gaussian

# all the differentiations and smoothings
window_size = 1000 # how much smoothoing is done and effects spacing between peaks
dGdf = np.gradient(Gaussian(amp, fre, pres), fre)
dGdf_smooth = np.convolve(dGdf, np.ones(window_size)/window_size, mode='same')
d2Gdf2 = np.gradient(dGdf_smooth, fre)
d2Gdf2_smooth = np.convolve(d2Gdf2, np.ones(window_size)/window_size, mode='same')
# above is just the main Gaussian below is all the Modulated GM = Gaussian Modulated
# GMS = the modulation was smoothed prior to taking the derivative (same process as IGOR)
mod_smooth = np.convolve(Gaussian_Mod, np.ones(window_size)/window_size, mode='same')
dGMdf = np.gradient(Gaussian_Mod, fre)
dGMSdf = np.gradient(mod_smooth, fre)
dGMdf_smooth = np.convolve(dGMdf, np.ones(window_size)/window_size, mode='same')
dGMSdf_smooth = np.convolve(dGMSdf, np.ones(window_size)/window_size, mode='same')
d2GMdf2 = np.gradient(dGMdf, fre)
d2GMSdf2 = np.gradient(dGMSdf, fre)
d2GMdf2_smooth = np.convolve(d2GMdf2, np.ones(window_size)/window_size, mode='same')
d2GMSdf2_smooth = np.convolve(d2GMSdf2, np.ones(window_size)/window_size, mode='same')


def makefigure(amp, fre, pres):
    fig, ax = plt.subplots(2, 1, figsize=(10, 20)) #dimentisons of the figure
    # base gaph --> no differentiation but has modulation
    ax[0].plot(fre_range, Gaussian_Mod, label = 'Origional + Not Smoothed Modulation')
    ax[0].plot(fre_range, mod_smooth, label='Original + Smoothed Modulation')
    ax[0].plot(fre_range, Gaussian(amp, fre, pres), label='y')
    ax[0].set_xlabel('Frequency (MHz)')
    ax[0].set_ylabel('Amplitude')
    ax[0].set_title('Collected Data')
    # second derivative and its modulations
    ax[1].plot(fre_range, d2GMdf2_smooth, label='d^2y/dx^2 + Not Smoothed Modulation')
    ax[1].plot(fre_range, d2GMSdf2_smooth, label='d^2y/dx^2 + Smoothed Modulation')
    ax[1].plot(fre_range, d2Gdf2_smooth, label = 'd^2y/dx^2') 
    ax[1].set_xlabel('Frequency (MHz)')
    ax[1].set_ylabel('Amplitude')
    ax[1].set_title('2nd Derivative')
    plt.legend()
    plt.show()
    # below is so we know what pressure, amplitude, modulation steps and cental steps are for this run
    print("For this run of the simmulation, the pressure is", pres, "mTorr. The central frequency is", fre, "MHz. The amplitude is", amp, ".")
    return()

makefigure(1, 183416, 18)
makefigure(amp, fre, pres)






