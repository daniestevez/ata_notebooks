#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import polarimetric_interferometry as pol

from ATATools import ata_control as ac

from gnuradio import gr

import sys
import signal
import time
import pmt
import logging

do_observation = False
antennas = ['1h', '4g']
lo = 'd'
if_switch_att = 20

obs_source = '3c286'
obs_freqs = [1413, 1665, 2675, 4820, 6663, 8665]
obs_period = 100

def park_antennas():
    logging.info('Parking antennas')
    if do_observation:
        ac.set_az_el(antennas, 0, 18)
    else:
        time.sleep(1)
    logging.info('Antennas parked')

def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    options = pol.argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        logging.warning("Error: failed to enable real-time scheduling.")
    tb = pol.flowgraph(directory=options.directory, gaindB=options.gaindB,
                           samp_rate=options.samp_rate, src_name=obs_source,
                           lo_freq = obs_freqs[0])
    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        park_antennas()
        logging.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    logging.info('Setting up feeds and IF switch')
    if do_observation:
        ac.try_on_lnas(antennas)
        ac.set_freq(obs_freqs[0], antennas, lo)
        ac.rf_switch_thread(antennas)
        ac.set_atten_thread([[f'{ant}x',f'{ant}y'] for ant in antennas],
                                [[if_switch_att,if_switch_att] for _ in antennas])
    else:
        time.sleep(1)
    logging.info('Feeds and IF set')

    logging.info(f'Slewing to source {obs_source}')
    if do_observation:
        ac.make_and_track_source(obs_source, antennas)
    else:
        time.sleep(1)
    logging.info(f'On source {obs_source}')

    logging.info('Running autotune')
    if do_observation:
        ac.autotune(antennas)
        logging.info(f'Detectors: {ac.get_dets(antennas)}')
        logging.info(f'PAMs: {ac.get_pams(antennas)}')
    else:
        time.sleep(1)
    logging.info('Autotune done')

    first_period = True
    while True:
        for freq in obs_freqs:
            if not first_period:
                logging.info(f'Setting LO {lo} to {freq} MHz')
                if do_observation:
                    ac.set_freq(freq, antennas, lo)
                else:
                    time.sleep(1)
                logging.info('LO set')
            else:
                logging.info(f'Starting first observation at {freq} MHz')

            logging.info('Starting recording')
            if first_period:
                first_period = False
                tb.make_sinks(freq)
                tb.start()
            else:
                tb.reload_sinks(freq)
                tb.unlock()
            
            time.sleep(obs_period)
            tb.lock()
            logging.info('Stopping recording')

if __name__ == '__main__':
    main()
