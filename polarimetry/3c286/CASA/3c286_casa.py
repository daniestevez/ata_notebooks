#!/usr/bin/env python3

#####################################################################
#
#  Non-polarimetric calibration of 3C286 observations
#
#  This script should be run with CASA 6.1.0
#
#####################################################################

import pathlib

# Import UVFITS files and concatenate as a single MS
uvfits = [str(s) for s in pathlib.Path('.').glob('3c286_*.uvfits')]
ms = [s.replace('uvfits', 'ms') for s in uvfits]

for uv, vis in zip(uvfits, ms):
    importuvfits(fitsfile = uv, vis = vis)
concat(vis = ms, concatvis = '3c286.ms')
for vis in ms:
    rmtables(vis)

vis = '3c286.ms'

# Set model flux density
setjy(vis = vis, spw = '0~1', model = '3C286_L.im')
setjy(vis = vis, spw = '2', model = '3C286_S.im')
setjy(vis = vis, spw = '3~4', model = '3C286_C.im')
setjy(vis = vis, spw = '5', model = '3C286_X.im')

# Automatic RFI flagging
# spw 1 shows strong RFI; the others are mostly clean
flagdata(vis='3c286.ms', mode='tfcrop', 
             datacolumn='data', action='apply', 
             flagbackup=False, freqcutoff = 4.0)

# Preliminary phase calibration
#
# For some reason this doesn't work if we do all spw's at once
# We do each spw completely separately and we append the results
#
# We use a larger solint for higher frequencie spw's, since they
# have less SNR
#
rmtables('3c286.G0')
for spw in range(6):
    gaincal(vis = vis, caltable = '3c286.G0',
                solint = '10' if spw < 4 else '30', preavg = 1,
                refant = '0', minblperant = 1, minsnr = 0,
                gaintype = 'G', calmode = 'p',
                spw = f'{spw}:64~192', append = True)

# Preliminary gain calibration
#
# Note this discards XX vs. YY signal difference and will
# be thrown away after solving delay and bandpass
gaincal(vis = vis, caltable = '3c286.G1', 
            solint = '100', preavg = 1, 
            refant = '0', minblperant = 1, minsnr = 0,
            gaintype = 'G', calmode = 'a',
            gaintable = ['3c286.G0'])
    
# Delay calibration
gaincal(vis = vis, caltable = '3c286.K0',
            solint = 'inf', combine = 'scan', preavg = 1,
            refant = '0', minblperant = 1,
            gaintype = 'K', spw = '*:16~240',
            gaintable = ['3c286.G0', '3c286.G1'])

# Bandpass calibration
#
# Different spws use different by channel averaging
# according to their lower SNR
rmtables('3c286.B0')
bandpass(vis = vis, caltable = '3c286.B0',
            solint = 'inf,2ch', combine = 'scan',
            refant = '0', minblperant = 1, minsnr = 0,
            bandtype = 'B', spw = '0~1',
            gaintable = ['3c286.G0', '3c286.G1', '3c286.K0'],
            append = True)
bandpass(vis = vis, caltable = '3c286.B0',
            solint = 'inf,4ch', combine = 'scan',
            refant = '0', minblperant = 1, minsnr = 0,
            bandtype = 'B', spw = '2',
            gaintable = ['3c286.G0', '3c286.G1', '3c286.K0'],
            append = True)
bandpass(vis = vis, caltable = '3c286.B0',
            solint = 'inf,8ch', combine = 'scan',
            refant = '0', minblperant = 1, minsnr = 0,
            bandtype = 'B', spw = '3~5',
            gaintable = ['3c286.G0', '3c286.G1', '3c286.K0'],
            append = True)

# Final amplitude and phase calibrations
#
# Phase and amplitude are solved independently
# For amplitude, we do a polarization-dependent calibration
# over all the scans to correct for the difference of
# gain in each channel and a polarization-independent
# calibration to compensate for gain changes with time
gaincal(vis = vis, caltable = '3c286.G2', 
            solint = '10', preavg = 1, 
            refant = '0', minblperant = 1, minsnr = 0,
            gaintype = 'G', calmode = 'p',
            spw = '*:16~240',
            gaintable = ['3c286.K0', '3c286.B0'])

gaincal(vis = vis, caltable = '3c286.G3',
            solint = 'inf', combine = 'scan', preavg = 1, 
            refant = '0', minblperant = 1, minsnr = 0,
            gaintype = 'G', calmode = 'a',
            spw = '*:16~240',
            gaintable = ['3c286.K0', '3c286.B0', '3c286.G2'])

gaincal(vis = vis, caltable = '3c286.T0', 
            solint = '10', preavg = 1, 
            refant = '0', minblperant = 1, minsnr = 0,
            gaintype = 'T', calmode = 'a',
            spw = '*:16~240',
            gaintable = ['3c286.K0', '3c286.B0', '3c286.G2', '3c286.G3'])

# Apply calibrations
applycal(vis = vis,
             gaintable = ['3c286.K0', '3c286.B0', '3c286.G2', '3c286.G3', '3c286.T0'],
             flagbackup = False)

# Write calibrated MS
#
# We use time and frequency averaging to reduce the size of the dataset
split(vis = vis, outputvis = '3c286_cal.ms',
          width = 8, timebin = '10s', datacolumn = 'corrected')

# Normalize calibrated data to unit flux
#
# Polarization calibration is easier with this normalization
gaincal(vis = '3c286_cal.ms', caltable = '3c286_cal.T0', 
            solint = 'inf', combine = 'scan', minblperant = 1,
            gaintype = 'T', calmode = 'a', smodel = [1, 0, 0, 0],
            parang = True)

rmtables('3c286_cal2.ms')
split(vis = '3c286_cal.ms', outputvis = '3c286_cal2.ms', datacolumn = 'data')
applycal(vis = '3c286_cal2.ms', gaintable = ['3c286_cal.T0'], flagbackup = False)
rmtables('3c286_cal_norm.ms')
split(vis = '3c286_cal2.ms', outputvis = '3c286_cal_norm.ms', datacolumn = 'corrected')
rmtables('3c286_cal2.ms')
             
# Extract XX and YY gain calibration for preliminary QU estimation
#
# This calibration file is then used by qufromgain() in CASA 5.5
for spw in range(6):
    gaincal(vis = '3c286_cal_norm.ms', caltable = f'3c286_cal_norm.spw{spw}.G0',
            solint = '50', smodel = [1, 0, 0, 0],
            gaintype = 'G', calmode = 'a', minsnr = 2,
            minblperant = 1, parang = True,
            preavg = 10, spw = f'{spw}')


# Calibrate cross-hand delay
gaincal(vis = '3c286_cal_norm.ms', caltable = '3c286_cal_norm.Kcross0',
            refant = '0', gaintype = 'KCROSS',
            solint = 'inf', combine = 'scan', calmode = 'ap',
            minblperant = 1, parang = True)
