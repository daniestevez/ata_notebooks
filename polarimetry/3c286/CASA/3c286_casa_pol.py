#!/usr/bin/env python2

#####################################################################
#
#  Non-polarimetric calibration of 3C286 observations
#
#  This script should be run with CASA 5.5.0
#
#  The procedure follows
#    https://casa.nrao.edu/casadocs/casa-5.5.0/calibration-and-visibility-data/
#    synthesis-calibration/instrumental-polarization-calibration
#
#####################################################################

from recipes.almapolhelpers import *
import numpy as np

vis = '3c286_cal_norm.ms'

# A priori estimate of QU from difference in XX and YY gain calibration
qu = list()
for spw in range(6):
    qu.append(qufromgain('3c286_cal_norm.spw{}.G0'.format(spw)))

# Ambiguous determination of XY phase offset and source QU
for spw in range(6):
    gaincal(vis = vis, caltable = '3c286_cal_norm.spw{}.xy0amb'.format(spw),
            solint = 'inf', combine = 'scan',
            preavg = 200,
            smodel = [1, 0, 1, 0], gaintype = 'XY+QU',
            minblperant = 1, spw = str(spw),
            gaintable = ['3c286_cal_norm.Kcross0'])

# Correct the ambiguous phase determination and construct source
# Stokes parameters model
S = [xyamb(xytab='3c286_cal_norm.spw{}.xy0amb'.format(spw),
                # for some reason the sign of qu needs to be inverted
                qu=(-qu[spw][0][0], -qu[spw][0][1]),
                xyout='3c286_cal_norm.spw{}.xy0'.format(spw))
                for spw in range(6)]

# Gain calibration with source Stokes parameter model
rmtables('3c286_cal_norm.G1')
for spw in range(6):
    gaincal(vis = vis, caltable = '3c286_cal_norm.G1',
                solint = '50', smodel = S[spw],
                gaintype = 'G', calmode = 'a',
                minblperant = 1, parang = True,
                preavg = 10, spw = str(spw),
                append = True,
                gaintable = ['3c286_cal_norm.Kcross0'])

# D-term calibration
rmtables('3c286_cal_norm.D0')
for spw in range(6):
    polcal(vis = vis, caltable = '3c286_cal_norm.D0',
               solint = 'inf', combine = 'scan',
               smodel = S[spw], spw = str(spw),
               preavg = 200, poltype = 'Dlls',
               refant = '',
               gaintable = ['3c286_cal_norm.G1', '3c286_cal_norm.Kcross0',
                                '3c286_cal_norm.spw{}.xy0'.format(spw)],
               append = True)

# Apply calibrations
for spw in range(6):
    applycal(vis = vis,
                gaintable = ['3c286_cal_norm.G1', '3c286_cal_norm.Kcross0',
                             '3c286_cal_norm.D0',
                             '3c286_cal_norm.spw{}.xy0'.format(spw)],
                 spw = str(spw),
                 parang = True)
