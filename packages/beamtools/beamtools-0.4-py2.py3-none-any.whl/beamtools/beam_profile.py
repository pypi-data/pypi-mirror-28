# -*- coding: utf-8 -*-
"""
Created on Wed Aug 3 11:31:57 2016

@author: cpkmanchee

beam_profile.py contains methods for dealing with beam profile images.
All definitions, usages, and calculations are consisten with ISO
standard 11146 (generally dealing with D4sigma beamwidths).
"""

import numpy as np
import scipy.optimize as opt
import uncertainties as un
import glob
import time

from beamtools.constants import h,c,pi
from beamtools.common import normalize
from beamtools.import_data_file import import_data_file as _import

#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
#from matplotlib.gridspec import GridSpec

__all__ = ['gaussian_beamwaist','fitM2',
            'get_roi','calculate_beamwidths','flattenrgb',
            'calculate_2D_moments','pix2um']


BITS = 8       #image channel intensity resolution
SATLIM = 0.001  #fraction of non-zero pixels allowed to be saturated
PIXSIZE = 1.745  #pixel size in um, measured


def _stop(string = 'error'): raise Exception(string)


def gaussian_beamwaist(z,z0,d0,M2=1,const=0,wl=1.030):
    '''Generate gaussian beam profile w(z), along optical axis.

    w(z) = w0*(1+((z-z0)/zR)^2)^(1/2)

    where zR is the Rayleigh length given by

    zR = pi*w0^2/wl

    Units for waist and wavelength is um.
    Units for optical axis positon is mm.

    Inputs:

        z = array of position along optical axis in mm
        z0 = position of beam waist (focus) in mm
        d0 = beam waist in um (diameter)
        M2 = beam parameter M^2, unitless
        wl =  wavelenth in um, default to 1030nm (1.03um)

    Outputs:

        w = w(z) position dependent beam waist in um. Same size as 'z'
    '''
    z = 1000*np.asarray(z).astype(float)
    z0 = 1000*z0
    w0 = d0/2
    
    w = (w0**2 + M2**2*(wl/(np.pi*w0))**2*(z-z0)**2)**(1/2) + const

    return w


def fitM2(dz, z, wl=1.03E-6):
    '''Fit series of beamwaists to gaussian beamwaist. 
    Follows ISO standard 11146 for fitting.

    Returns gaussian beam paramters with uncertainties.

    Inputs:
        z, position aling optical axis in mm
        dz, beamwidth in um, = 2*w, i.e. dz is beam diameter
        wl, (optional) wavelength, default = 1030nm

    a,b, and c are fit parameters

    Outputs:
        z0,d0,M2,theta,zR and associated uncertainties.
    '''
    dz = dz*1E-6
    z = z*1E-3
    
    #initial paramters for fit
    di = np.min(dz)
    zi = z[np.argmin(dz)]
    ci = (wl/(np.pi*di))**2
    bi = -2*zi*ci
    ai = di**2 + ci*zi**2
    
    #fit limits
    c_lim = np.array([0, np.inf])
    b_lim = np.array([-np.inf,np.inf])
    a_lim = np.array([0, np.inf])

    p0 = [ai, bi, ci]
    limits = ([i.min() for i in [a_lim,b_lim,c_lim]],  [i.max() for i in [a_lim,b_lim,c_lim]])

    f = lambda z,a,b,c: (a + b*z + c*z**2)**(1/2) 
    popt,pcov = opt.curve_fit(f,z,dz,p0,bounds=limits)
    [a,b,c] = [un.ufloat(popt[i], np.sqrt(pcov[i,i])) for i in range(3)]

    z0 = (1E3)*(-b/(2*c))
    d0 = (1E6)*((4*a*c-b**2)**(1/2))*(1/(2*c**(1/2)))
    M2 = (np.pi/(8*wl))*((4*a*c-b**2)**(1/2))
    theta = c**(1/2)
    zR = (1E3)*((4*a*c-b**2)**(1/2))*(1/(2*c))

    value = [x.nominal_value for x in [z0,d0,M2,theta,zR]]
    std = [x.std_dev for x in [z0,d0,M2,theta,zR]]

    return value, std
    

def flattenrgb(im, bits=8, satlim=0.001):
    '''Flattens rbg array, excluding saturated channels
    '''

    sat_det = np.zeros(im.shape[2])
    
    Nnnz = np.zeros(im.shape[2])
    Nsat = np.zeros(im.shape[2])
    data = np.zeros(im[...,0].shape, dtype = 'uint32')

    for i in range(im.shape[2]):
        
        Nnnz[i] = (im[:,:,i] != 0).sum()
        Nsat[i] = (im[:,:,i] >= 2**bits-1).sum()
        
        if Nsat[i]/Nnnz[i] <= satlim:
            data += im[:,:,i]
        else:
            sat_det[i] = 1
    
    output = normalize(data.astype(float))

    return output, sat_det
    

def calculate_beamwidths(data, error_limit=1E-4, it_limit=5):
    '''Calculate beam profile parameters, ISO standard 11146
    data = image matrix

    data,x,y all same dimensions
    '''

    errx = 1
    erry = 1
    itN = 0

    d0x = data.shape[1]
    d0y = data.shape[0]

    roi_new = [d0x/2,d0x,d0y/2,d0y]
    full_data = data

    while any([i>error_limit for i in [errx,erry]]):

        roi = roi_new
        data = get_roi(full_data,roi)
        moments = calculate_2D_moments(data)

        dx = 4*np.sqrt(moments[2])
        dy = 4*np.sqrt(moments[3])

        errx = np.abs(dx-d0x)/d0x
        erry = np.abs(dy-d0y)/d0y
        
        d0x = dx
        d0y = dy

        roi_new = [moments[0]+roi[0]-roi[1]/2,3*dx,moments[1]+roi[2]-roi[3]/2,3*dy]     #[centrex,width,centrey,height] 
        
        itN += 1
        if itN >= it_limit:
            print('exceeded iteration in calculating moments')
            break
   
    pixel_scale = [pix2um(1)]*2+ [pix2um(1)**2]*3
    moments = pixel_scale*moments
    [ax,ay,s2x,s2y,s2xy] = moments


    g = np.sign(s2x-s2y)
    dx = 2*np.sqrt(2)*((s2x+s2y) + g*((s2x-s2y)**2 + 4*s2xy**2)**(1/2))**(1/2)
    dy = 2*np.sqrt(2)*((s2x+s2y) - g*((s2x-s2y)**2 + 4*s2xy**2)**(1/2))**(1/2)

    if s2x == s2y:
        phi = (np.pi/4)*np.sign(s2xy)
    else:
        phi = (1/2)*np.arctan(2*s2xy/(s2x-s2y))

    beamwidths = [dx,dy,phi]

    return beamwidths,roi,moments


def calculate_2D_moments(data, axes_scale=[1,1], calc_2nd_moments = True):
    '''
    data = 2D data
    axes_scale = (optional) scaling factor for x and y

    returns first and second moments

    first moments are averages in each direction
    second moments are variences in x, y and diagonal
    '''
    x = axes_scale[0]*(np.arange(data.shape[1]))
    y = axes_scale[1]*(np.arange(data.shape[0]))
    dx,dy = np.meshgrid(np.gradient(x),np.gradient(y))
    x,y = np.meshgrid(x,y)

    A = np.sum(data*dx*dy)
    
    #first moments (averages)
    avgx = np.sum(data*x*dx*dy)/A
    avgy = np.sum(data*y*dx*dy)/A

    #calculate second moments if required
    if calc_2nd_moments:
        #second moments (~varience)
        sig2x = np.sum(data*(x-avgx)**2*dx*dy)/A
        sig2y = np.sum(data*(y-avgy)**2*dx*dy)/A
        sig2xy = np.sum(data*(x-avgx)*(y-avgy)*dx*dy)/A
        
        return np.array([avgx,avgy,sig2x,sig2y,sig2xy])

    else:
        return np.array([avgx, avgy])


def get_roi(data,roi):
    '''
    data = 2D data
    roi = [x0,width,y0,height]
    '''
    
    left = roi[0] - roi[1]/2
    bottom = roi[2] - roi[3]/2
    width = roi[1]
    height = roi[3]

    left = min(left,data.shape[1]-2)
    if left <= 0:
        width += left
        left = 0
    elif np.isnan(left):
        left=0
    else:
        left = np.int(left)

    bottom = min(bottom,data.shape[0]-2)
    if bottom <= 0:
        height += bottom
        bottom = 0
    elif np.isnan(bottom):
        bottom = 0
    else:
        bottom = np.int(bottom)

    if left+width > data.shape[1]:
        width = np.int(data.shape[1] - left)
    elif np.isnan(width):
        width = data.shape[1]
    else:
        width = np.int(width)

    if bottom+height > data.shape[0]:
        height = np.int(data.shape[0] - bottom)
    elif np.isnan(height):
        height = data.shape[0]
    else:
        height = np.int(height)

    return data[bottom:bottom+height,left:left+width]



def pix2um(input):

    if np.isscalar(input):
        output = input*PIXSIZE
    else:
        output =  [x*PIXSIZE for x in input]

    return output


def open_profile(filename, raw=False):
    '''Import beam profile image file.
    If raw = true, the raw image is return, otherwise flattened image is 
    returned. Channel (RGB) saturation data is always returned.
    '''
    im = plt.imread(f)
    data, sat = flattenrgb(im, BITS, SATLIM)

    if raw:
        return im, sat
    else:
        return data, sat


def knife_edge(datafile):
    '''Analyze knife edge data. Return analysis results and raw data.
    '''
    data = _import(datafile, 'bt_knifeedge')
    x = data.position
    power = data.power

    profile = normalize(-np.gradient(power,np.gradient(x)))

    avgx = np.average(x, weights = profile)
    sig = np.sqrt(np.sum(profile*(x-avgx)**2)/profile.sum())

    results = [profile,avgx,sig]

    return results, data
    

def m2analysis(directory):
    '''Complete M2 analysis
    '''
    files = glob.glob(directory+'/*.jp*g')

    # Consistency check, raises error if failure
    if not files:
        _stop('No files found... try again, but be better')

    try:
        z = np.loadtxt(directory + '/position.txt', skiprows = 1)
        z = 2*z
    except (AttributeError, FileNotFoundError):
        _stop('No position file found --> best be named "position.txt"')
        
    if np.size(files) is not np.size(z):
        _stop('# of images does not match positions - fix ASAP')

    #output parameters
    beam_stats = []
    chl_sat = []
    img_roi = []

    for f in files:
        
        im = plt.imread(f)
        data, sat = flattenrgb(im, BITS, SATLIM)

        d4stats, roi , _ = calculate_beamwidths(data)

        beam_stats += [d4stats]
        chl_sat += [sat]
        img_roi += [roi]


        
    beam_stats = np.asarray(beam_stats)
    chl_sat = np.asarray(chl_sat)
    img_roi = np.asarray(img_roi)

    #x and y beam widths
    d4x = beam_stats[:,0]
    d4y = beam_stats[:,1]

    #fit to gaussian mode curve
    valx, stdx = fitM2(d4x,z)
    valy, stdy = fitM2(d4y,z)

    #obtain 'focus image'
    focus_number = np.argmin(np.abs(valx[0]-z))
    Z = z-valx[0]

    im = plt.imread(files[focus_number])
    data, SAT = flattenrgb(im, BITS, SATLIM)
    data = normalize(get_roi(data.astype(float), img_roi[focus_number]))

    x = pix2um(1)*(np.arange(data.shape[1]) - data.shape[1]/2)
    y = pix2um(1)*(np.arange(data.shape[0]) - data.shape[0]/2)
    X,Y = np.meshgrid(x,y)

  