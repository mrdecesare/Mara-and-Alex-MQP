#libraries needed to exicute the code
import numpy as np
import random 
import matplotlib.pyplot as plt 
###############################################################################

#random values for each of the variables we control for the expirament 
#the min and max values are set according to the system in the lab
amp = np.random.uniform(0.1, 10)  
fre = random.randint(183000, 185000)#in MHz, cannot do GHz because wont work
fre_s = fre - 10
fre_e = fre + 10
fre_range = np.linspace(fre_s, fre_e, 50000) #we want the sweep to be 20 MHz thats what this does
pres = random.randint(1, 200) #safe range to complete the expirament in Torr 
    #cause this function doesnt allow you to go smaller then 1 
    #if we say the values are in mTorr then the curve is way too wide
 
def G(amp, fre, pres): 
    x = fre_range # simplifies the variable for the frequency range equation just for the function
    g = -amp*np.exp(-(x-fre)**2/(2*(pres/1000)**2)) #eq for gaussian curve 
    # x-fre--> position of the center of the gaussian curve
    # pres/1000 --> converts the pressure into mTorr for more accurate gaussian curve
    return(g)

window_size = 1000 #how musch smoothing is done (set to approx the same as it is in igor)

#first and second derivative of the gaussian function
dGdf = np.gradient(G(amp, fre, pres), fre)
dGdf_smooth = np.convolve(dGdf, np.ones(window_size)/window_size, mode='same')
d2Gdf2 = np.gradient(dGdf_smooth, fre)
d2Gdf2_smooth = np.convolve(d2Gdf2, np.ones(window_size)/window_size, mode='same')


#making a function for the figure output
def figu(amp, fre, pres):
    fig, ax = plt.subplots(3, 1, figsize=(10, 20)) #dimentisons of the figure
    ax[0].plot(fre_range, G(amp, fre, pres), label='y')
    ax[0].set_xlabel('freq(MHz)')
    ax[0].set_ylabel('amplitude')
    ax[0].set_title('collected data')
    ax[1].plot(fre_range, dGdf_smooth, label='dy/dx')
    ax[1].set_xlabel('freq(MHz)')
    ax[1].set_ylabel('amplitude')
    ax[1].set_title('1st derivative')
    ax[2].plot(fre_range, d2Gdf2_smooth, label = '$$d^2y/dx^2$$')
    ax[2].set_xlabel('freq(MHz)')
    ax[2].set_ylabel('amplitude')
    ax[2].set_title('2nd derivative')                                        
    plt.show()
    return()

figu(amp, fre, pres)


