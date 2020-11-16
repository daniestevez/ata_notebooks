#!/usr/bin/env python3

plotms(vis = '3c286.K0', xaxis = 'frequency', yaxis = 'delay', antenna='"1"',
           coloraxis = 'corr', plotfile = '/tmp/3c826_casa_K0.png')

plotms(vis = '3c286.B0', xaxis = 'frequency', yaxis = 'phase', antenna='0',
           gridrows = 2, gridcols = 3, iteraxis = 'spw', coloraxis = 'corr',
           plotfile = '/tmp/3c826_casa_B0_phase0.png')

plotms(vis = '3c286.B0', xaxis = 'frequency', yaxis = 'phase', antenna='"1"',
           gridrows = 2, gridcols = 3, iteraxis = 'spw', coloraxis = 'corr',
           plotfile = '/tmp/3c826_casa_B0_phase1.png')

plotms(vis = '3c286.B0', xaxis = 'frequency', yaxis = 'phase', antenna='"1"',
           gridrows = 2, gridcols = 3, iteraxis = 'spw', coloraxis = 'corr',
           plotfile = '/tmp/3c826_casa_B0_phase1.png')

plotms(vis = '3c286.G2', xaxis = 'time', yaxis = 'phase', antenna='"1"',
           coloraxis='corr', iteraxis = 'spw', plotrange=[-1,-1,-180,180],
           gridrows = 2, gridcols = 3, plotfile = '/tmp/3c286_casa_phase.png')

plotms(vis = '3c286.G3', xaxis = 'frequency', yaxis = 'amplitude',
           iteraxis = 'antenna', coloraxis='corr', gridrows = 2,
           plotfile = '/tmp/3c286_casa_antenna_gain.png')

plotms(vis = '3c286.T0', xaxis = 'time', yaxis = 'amplitude',
           coloraxis='corr', iteraxis = 'spw',
           gridrows = 2, gridcols = 3,
           plotfile = '/tmp/3c286_casa_tropo.png')

plotms(vis = '3c286_cal.ms', xaxis = 'time', yaxis = 'phase', coloraxis = 'spw',
           iteraxis = 'corr', avgchannel = '256',
           gridrows = 2, gridcols = 2,
           plotrange =[-1,-1,-180,180],
           plotfile = '/tmp/3c286_cal_phase.png')

 plotms(vis = '3c286_cal.ms', xaxis = 'time', yaxis = 'amplitude',
            coloraxis = 'spw', iteraxis = 'corr', avgchannel = '256',
            gridrows = 2, gridcols = 2,
            plotfile = '/tmp/3c286_cal_amp.png')

 plotms(vis = '3c286_cal_norm.spw0.G0', xaxis = 'time',
            yaxis = 'amplitude', coloraxis = 'corr',
            antenna = '"1"', plotfile = '/tmp/3c286_polarimetric_gain.png')

plotms(vis = '3c286_cal_norm.G1', xaxis = 'time',
           yaxis = 'amplitude', coloraxis = 'corr',
           iteraxis = 'spw', gridrows = 2, gridcols = 3,
           plotfile = '/tmp/3c286_parallactic_gain.png')


plotms(vis = '3c286_cal_norm.ms', xaxis = 'time', yaxis = 'phase',
           coloraxis = 'spw', iteraxis = 'corr', avgchannel = '256',
           gridrows = 2, gridcols = 2, plotrange =[-1,-1,-180,180],
           ydatacolumn = 'corrected', plotfile = '/tmp/3c286_polcal_phase.png')
