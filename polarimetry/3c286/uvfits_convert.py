#!/usr/bin/env python3

import pyuvdata
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.time import Time, TimeDelta

import pathlib
import sys

def usage():
    print(f'Usage: {sys.argv[0]} input_dir output_dir')
    exit(1)


if len(sys.argv) != 3:
    usage()
    
path = pathlib.Path(sys.argv[1])
frequencies = [float(str(s).split('.')[1]) for s in path.glob('uv.*.npz')]

baseline_m = [-172.93166+0.2, -56.959799+0.2, -159.80786]
fs = 30.72e6
nfft = 256

for freq in frequencies:
    fc = freq * 1e6
    jds = np.load(path / f'jd.{freq:.0f}.npy')
    uv = list(np.load(path / f'uv.{freq:.0f}.npz').values())
    uvw = list(np.load(path / f'uvw.{freq:.0f}.npz').values())

    UV = pyuvdata.UVData()
    UV.telescope_location_lat_lon_alt_degrees = np.array([40.8174, -121.472, 1043])
    UV.instrument = 'gnuradio1'
    UV.telescope_name = 'ATA'
    UV.object_name = '3C286'
    UV.history = ''
    UV.vis_units = 'UNCALIB'
    UV._set_phased()
    coords = SkyCoord.from_name(UV.object_name)
    UV.phase_center_ra = coords.ra.rad
    UV.phase_center_dec = coords.dec.rad
    UV.phase_center_epoch = 2000.0
    UV.Nants_data = 2
    UV.Nants_telescope = 2
    UV.Ntimes = int(np.sum([x.shape[1] for x in uv]))
    UV.ant_1_array = np.empty(UV.Ntimes, dtype = 'int')
    UV.ant_1_array[:] = 0
    UV.ant_2_array = np.empty(UV.Ntimes, dtype = 'int')
    UV.ant_2_array[:] = 1
    UV.antenna_names = ['1h', '4g']
    UV.antenna_numbers = np.array([0,1])
    UV.antenna_positions = np.array([[0,0,0], baseline_m], dtype = 'float')
    UV.baseline_array = UV.antnums_to_baseline(UV.ant_1_array, UV.ant_2_array)
    UV.Nbls = len(np.unique(UV.baseline_array))
    UV.time_array = np.concatenate([jd + np.arange(x.shape[1])/(24*3600)*0.1 for jd,x in zip(jds,uv)])
    UV.integration_time = np.empty(UV.time_array.size)
    UV.integration_time[:] = 0.1
    UV.set_lsts_from_time_array()
    UV.freq_array = np.array([fc + np.fft.fftshift(np.fft.fftfreq(nfft, 1/fs))])
    UV.spw_array = np.array([0])
    UV.channel_width = fs/nfft
    UV.polarization_array = np.array([-5,-6,-7,-8], dtype = 'int')
    UV.Nfreqs = UV.freq_array.size
    UV.Npols = UV.polarization_array.size
    UV.Nblts = UV.Nbls * UV.Ntimes
    UV.Nspws = UV.spw_array.size
    UV.uvw_array = np.zeros((UV.Nblts, 3), dtype = 'float')
    UV.uvw_array[:] = np.concatenate(uvw, axis = 1).T

    UV.data_array = np.zeros((UV.Nblts, 1, UV.Nfreqs, UV.Npols), dtype = 'complex')
    UV.flag_array = np.zeros((UV.Nblts, 1, UV.Nfreqs, UV.Npols), dtype = 'bool')
    UV.nsample_array = np.empty((UV.Nblts, 1, UV.Nfreqs, UV.Npols), dtype = 'float')
    UV.nsample_array[:] = fs * 0.1

    UV.data_array[:] = np.einsum('ijk->jki', np.concatenate(uv, axis = 1))[:,np.newaxis,:,[0,3,1,2]]
    
    # correct for weird rotECEF convention
    UV.antenna_positions = pyuvdata.utils.ECEF_from_rotECEF(UV.antenna_positions,
                                                        UV.telescope_location_lat_lon_alt[1])
    UV.write_uvfits(f'{sys.argv[2]}/3c286_{freq:.0f}.uvfits',
                    force_phase=True, spoof_nonessential=True)
