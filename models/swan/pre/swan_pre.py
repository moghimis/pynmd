# -*- coding: utf-8 -*-
"""
Tools to manage swan input

External dependencies:
  netCDF4, getpass, time, os, sys, numpy

Internal dependencies:

"""

# Heading management
from __future__ import division,print_function,absolute_import

__author__ = "Gabriel Garcia Medina"

# Import modules

# Import pynmd modules

#===============================================================================
# Write SWAN input spectrum
#===============================================================================
def write_boundary_spec(freq,spec,locations,outfile,waveTime=None,
                        sdir=None):
    """
    
    PARAMETERS:
    -----------
    freq      : 1D frequency vector
    spec      : Spectra matrix
                Dimensions: time,locations,frequency,direction
                Units: m2/Hz/degrees
    locations : 2 column matrix with locations. 
                Dimensions: npts,2                 
    outfile   : output file
    waveTime  : Time vector, if needed
    sdir      : 1D direction vector, if needed
       
    OUTPUT:
    -------
    writes a SWAN compatible spectra file
    
    EXAMPLE:
    --------
    >>> spec.shape[0]
    
    NOTES:
    ------
    - Not fully tested, still work in progress but no time.
    - If 1D spectrum make sure that spec.shape = nfreq,1    
    
    TODO:
    -----
    - Add relative or absolute frequency
    - Add flag for cartesian or nautical convention
    
    """
       
    # Open the output file
    fid = open(outfile,'w')
    
    # Write file header
    fid.write('SWAN 1\n')
    
    # File locations
    fid.write('LOCATIONS\n')
    fid.write('%12.0f' % locations.shape[0] + '\n')
    for aa in range(locations.shape[0]):
        fid.write('%16.4f' % locations[aa,0] + ' ' + 
                  '%16.4f' % locations[aa,1] + '\n')
    
    # Frequencies
    fid.write('RFREQ\n')
    fid.write('%12.0f' % freq.shape[0] + '\n')
    for aa in range(freq.shape[0]):
        fid.write('%12.8f' % freq[aa] + '\n')
    
    # Directions
    if sdir is not None:
        fid.write('NDIR\n')
        fid.write('%12.0f' % sdir.shape[0] + '\n')
        for aa in range(sdir.shape[0]):
            fid.write('%16.4f' % sdir[aa] + '\n')
    
    # Number of quantities in table
    fid.write('QUANT\n')
    fid.write('1\n')
    
    # Variance density
    fid.write('VaDens\n')
    fid.write('m2/Hz/degr\n')
    
    # Exception value
    fid.write('-99\n')
    
    # Scale factor
    fid.write('FACTOR\n')
    fid.write('1\n')
    
    # Print the spectrum -----------------------
    # Frequency loop
    for aa in range(spec.shape[-2]):
        # Direction loop
        for bb in range(spec.shape[-1]):
            fid.write('%16.10f' % spec[aa,bb])
        # One row per frequency with all directions
        fid.write('\n')

    # Close the file
    fid.close()
    