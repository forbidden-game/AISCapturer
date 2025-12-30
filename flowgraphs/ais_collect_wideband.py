#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: AIS Collect Wideband
# Description: AIS wideband capture + split + verify
# GNU Radio version: 3.8.5.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
import ais
import epy_block_stats_ais1
import epy_block_stats_ais2

from gnuradio import qtgui

class ais_collect_wideband(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "AIS Collect Wideband")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("AIS Collect Wideband")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "ais_collect_wideband")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.seg_secs = seg_secs = 10
        self.samp_rate = samp_rate = 2e6
        self.out_dir = out_dir = "/home/pan/expri/gnuradio/collect_AIS/captures"
        self.decim = decim = 10
        self.chan_trans = chan_trans = 5e3
        self.chan_bw = chan_bw = 12.5e3
        self.base_name_ais2 = base_name_ais2 = "AIS2_200kSps"
        self.base_name_ais1 = base_name_ais1 = "AIS1_200kSps"
        self.ais_sym_rate = ais_sym_rate = 9600
        self.ais_sps = ais_sps = 5
        self.xlating_taps = xlating_taps = firdes.low_pass(1.0, samp_rate, chan_bw, chan_trans)
        self.samples_per_file = samples_per_file = int(samp_rate * seg_secs)
        self.rx_gain = rx_gain = 30
        self.resamp_interp = resamp_interp = 12
        self.resamp_decim = resamp_decim = 50
        self.out_file_ais2 = out_file_ais2 = out_dir + "/" + base_name_ais2 + "_" + time.strftime("%Y%m%d_%H%M%S") + ".sigmf-data"
        self.out_file_ais1 = out_file_ais1 = out_dir + "/" + base_name_ais1 + "_" + time.strftime("%Y%m%d_%H%M%S") + ".sigmf-data"
        self.chan_rate = chan_rate = samp_rate/decim
        self.center_freq = center_freq = 162e6
        self.ant = ant = "RX2"
        self.ais_demod_rate = ais_demod_rate = ais_sym_rate*ais_sps
        self.ais2_offset = ais2_offset = 25e3
        self.ais1_offset = ais1_offset = -25e3

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args="",
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_source_0.set_rx_agc(False, 0)
        self.uhd_usrp_source_0.set_gain(rx_gain, 0)
        self.uhd_usrp_source_0.set_antenna(ant, 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        # No synchronization enforced.
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=resamp_interp,
                decimation=resamp_decim,
                taps=None,
                fractional_bw=0.4)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=resamp_interp,
                decimation=resamp_decim,
                taps=None,
                fractional_bw=0.4)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            center_freq, #fc
            samp_rate, #bw
            "Wideband Waterfall", #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "Wideband Time", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_ais2 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_ais2.set_update_time(0.5)
        self.qtgui_number_sink_ais2.set_title("AIS2 CRC OK FPS")

        labels = ['AIS2 CRC_OK FPS', '', '', '', '',
            '', '', '', '', '']
        units = ['fps', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_ais2.set_min(i, 0)
            self.qtgui_number_sink_ais2.set_max(i, 50)
            self.qtgui_number_sink_ais2.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_ais2.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_ais2.set_label(i, labels[i])
            self.qtgui_number_sink_ais2.set_unit(i, units[i])
            self.qtgui_number_sink_ais2.set_factor(i, factor[i])

        self.qtgui_number_sink_ais2.enable_autoscale(True)
        self._qtgui_number_sink_ais2_win = sip.wrapinstance(self.qtgui_number_sink_ais2.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_ais2_win)
        self.qtgui_number_sink_ais1 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_ais1.set_update_time(0.5)
        self.qtgui_number_sink_ais1.set_title("AIS1 CRC OK FPS")

        labels = ['AIS1 CRC_OK FPS', '', '', '', '',
            '', '', '', '', '']
        units = ['fps', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_ais1.set_min(i, 0)
            self.qtgui_number_sink_ais1.set_max(i, 50)
            self.qtgui_number_sink_ais1.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_ais1.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_ais1.set_label(i, labels[i])
            self.qtgui_number_sink_ais1.set_unit(i, units[i])
            self.qtgui_number_sink_ais1.set_factor(i, factor[i])

        self.qtgui_number_sink_ais1.enable_autoscale(True)
        self._qtgui_number_sink_ais1_win = sip.wrapinstance(self.qtgui_number_sink_ais1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_ais1_win)
        self.qtgui_freq_sink_x_2 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            chan_rate, #bw
            "AIS2 Spectrum", #name
            1
        )
        self.qtgui_freq_sink_x_2.set_update_time(0.10)
        self.qtgui_freq_sink_x_2.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_2.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_2.enable_autoscale(False)
        self.qtgui_freq_sink_x_2.enable_grid(False)
        self.qtgui_freq_sink_x_2.set_fft_average(1.0)
        self.qtgui_freq_sink_x_2.enable_axis_labels(True)
        self.qtgui_freq_sink_x_2.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_2.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_2_win = sip.wrapinstance(self.qtgui_freq_sink_x_2.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_2_win, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            chan_rate, #bw
            "AIS1 Spectrum", #name
            1
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_1_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            2048, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            center_freq, #fc
            samp_rate, #bw
            "Wideband Spectrum", #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.freq_xlating_fir_filter_xxx_1 = filter.freq_xlating_fir_filter_ccf(decim, xlating_taps, ais2_offset, samp_rate)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccf(decim, xlating_taps, ais1_offset, samp_rate)
        self.epy_block_stats_ais2 = epy_block_stats_ais2.PduStats()
        self.epy_block_stats_ais1 = epy_block_stats_ais1.PduStats()
        self.digital_hdlc_deframer_bp_1 = digital.hdlc_deframer_bp(11, 64)
        self.digital_hdlc_deframer_bp_0 = digital.hdlc_deframer_bp(11, 64)
        self.blocks_throttle_stats_ais2 = blocks.throttle(gr.sizeof_float*1, 2,True)
        self.blocks_throttle_stats_ais1 = blocks.throttle(gr.sizeof_float*1, 2,True)
        self.blocks_message_debug_1 = blocks.message_debug()
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_file_sink_ais2 = blocks.file_sink(gr.sizeof_gr_complex*1, out_file_ais2, False)
        self.blocks_file_sink_ais2.set_unbuffered(False)
        self.blocks_file_sink_ais1 = blocks.file_sink(gr.sizeof_gr_complex*1, out_file_ais1, False)
        self.blocks_file_sink_ais1.set_unbuffered(False)
        self.ais_pdu_to_nmea_1 = ais.pdu_to_nmea("B")
        self.ais_pdu_to_nmea_0 = ais.pdu_to_nmea("A")
        self.ais_demod_1 = ais.ais_demod({
            "samples_per_symbol": ais_sps,
            "bits_per_sec": ais_sym_rate,
            "clockrec_gain": 0.04,
            "omega_relative_limit": 0.01,
            "fftlen": 1024,
        })
        self.ais_demod_0 = ais.ais_demod({
            "samples_per_symbol": ais_sps,
            "bits_per_sec": ais_sym_rate,
            "clockrec_gain": 0.04,
            "omega_relative_limit": 0.01,
            "fftlen": 1024,
        })


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.ais_pdu_to_nmea_0, 'out'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.ais_pdu_to_nmea_1, 'out'), (self.blocks_message_debug_1, 'print'))
        self.msg_connect((self.digital_hdlc_deframer_bp_0, 'out'), (self.ais_pdu_to_nmea_0, 'to_nmea'))
        self.msg_connect((self.digital_hdlc_deframer_bp_0, 'out'), (self.epy_block_stats_ais1, 'in'))
        self.msg_connect((self.digital_hdlc_deframer_bp_1, 'out'), (self.ais_pdu_to_nmea_1, 'to_nmea'))
        self.msg_connect((self.digital_hdlc_deframer_bp_1, 'out'), (self.epy_block_stats_ais2, 'in'))
        self.connect((self.ais_demod_0, 0), (self.digital_hdlc_deframer_bp_0, 0))
        self.connect((self.ais_demod_1, 0), (self.digital_hdlc_deframer_bp_1, 0))
        self.connect((self.blocks_throttle_stats_ais1, 0), (self.qtgui_number_sink_ais1, 0))
        self.connect((self.blocks_throttle_stats_ais2, 0), (self.qtgui_number_sink_ais2, 0))
        self.connect((self.epy_block_stats_ais1, 0), (self.blocks_throttle_stats_ais1, 0))
        self.connect((self.epy_block_stats_ais2, 0), (self.blocks_throttle_stats_ais2, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_file_sink_ais1, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.blocks_file_sink_ais2, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.qtgui_freq_sink_x_2, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.ais_demod_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.ais_demod_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.freq_xlating_fir_filter_xxx_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ais_collect_wideband")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_seg_secs(self):
        return self.seg_secs

    def set_seg_secs(self, seg_secs):
        self.seg_secs = seg_secs
        self.set_samples_per_file(int(self.samp_rate * self.seg_secs))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_chan_rate(self.samp_rate/self.decim)
        self.set_samples_per_file(int(self.samp_rate * self.seg_secs))
        self.set_xlating_taps(firdes.low_pass(1.0, self.samp_rate, self.chan_bw, self.chan_trans))
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_out_dir(self):
        return self.out_dir

    def set_out_dir(self, out_dir):
        self.out_dir = out_dir
        self.set_out_file_ais1(self.out_dir + "/" + self.base_name_ais1 + "_" + time.strftime("%Y%m%d_%H%M%S") + ".sigmf-data")
        self.set_out_file_ais2(self.out_dir + "/" + self.base_name_ais2 + "_" + time.strftime("%Y%m%d_%H%M%S") + ".sigmf-data")

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim
        self.set_chan_rate(self.samp_rate/self.decim)

    def get_chan_trans(self):
        return self.chan_trans

    def set_chan_trans(self, chan_trans):
        self.chan_trans = chan_trans
        self.set_xlating_taps(firdes.low_pass(1.0, self.samp_rate, self.chan_bw, self.chan_trans))

    def get_chan_bw(self):
        return self.chan_bw

    def set_chan_bw(self, chan_bw):
        self.chan_bw = chan_bw
        self.set_xlating_taps(firdes.low_pass(1.0, self.samp_rate, self.chan_bw, self.chan_trans))

    def get_base_name_ais2(self):
        return self.base_name_ais2

    def set_base_name_ais2(self, base_name_ais2):
        self.base_name_ais2 = base_name_ais2
        self.set_out_file_ais2(self.out_dir + "/" + self.base_name_ais2 + "_" + time.strftime("%Y%m%d_%H%M%S") + ".sigmf-data")

    def get_base_name_ais1(self):
        return self.base_name_ais1

    def set_base_name_ais1(self, base_name_ais1):
        self.base_name_ais1 = base_name_ais1
        self.set_out_file_ais1(self.out_dir + "/" + self.base_name_ais1 + "_" + time.strftime("%Y%m%d_%H%M%S") + ".sigmf-data")

    def get_ais_sym_rate(self):
        return self.ais_sym_rate

    def set_ais_sym_rate(self, ais_sym_rate):
        self.ais_sym_rate = ais_sym_rate
        self.set_ais_demod_rate(self.ais_sym_rate*self.ais_sps)

    def get_ais_sps(self):
        return self.ais_sps

    def set_ais_sps(self, ais_sps):
        self.ais_sps = ais_sps
        self.set_ais_demod_rate(self.ais_sym_rate*self.ais_sps)

    def get_xlating_taps(self):
        return self.xlating_taps

    def set_xlating_taps(self, xlating_taps):
        self.xlating_taps = xlating_taps
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.xlating_taps)
        self.freq_xlating_fir_filter_xxx_1.set_taps(self.xlating_taps)

    def get_samples_per_file(self):
        return self.samples_per_file

    def set_samples_per_file(self, samples_per_file):
        self.samples_per_file = samples_per_file

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)

    def get_resamp_interp(self):
        return self.resamp_interp

    def set_resamp_interp(self, resamp_interp):
        self.resamp_interp = resamp_interp

    def get_resamp_decim(self):
        return self.resamp_decim

    def set_resamp_decim(self, resamp_decim):
        self.resamp_decim = resamp_decim

    def get_out_file_ais2(self):
        return self.out_file_ais2

    def set_out_file_ais2(self, out_file_ais2):
        self.out_file_ais2 = out_file_ais2
        self.blocks_file_sink_ais2.open(self.out_file_ais2)

    def get_out_file_ais1(self):
        return self.out_file_ais1

    def set_out_file_ais1(self, out_file_ais1):
        self.out_file_ais1 = out_file_ais1
        self.blocks_file_sink_ais1.open(self.out_file_ais1)

    def get_chan_rate(self):
        return self.chan_rate

    def set_chan_rate(self, chan_rate):
        self.chan_rate = chan_rate
        self.qtgui_freq_sink_x_1.set_frequency_range(0, self.chan_rate)
        self.qtgui_freq_sink_x_2.set_frequency_range(0, self.chan_rate)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.uhd_usrp_source_0.set_center_freq(self.center_freq, 0)

    def get_ant(self):
        return self.ant

    def set_ant(self, ant):
        self.ant = ant
        self.uhd_usrp_source_0.set_antenna(self.ant, 0)

    def get_ais_demod_rate(self):
        return self.ais_demod_rate

    def set_ais_demod_rate(self, ais_demod_rate):
        self.ais_demod_rate = ais_demod_rate

    def get_ais2_offset(self):
        return self.ais2_offset

    def set_ais2_offset(self, ais2_offset):
        self.ais2_offset = ais2_offset
        self.freq_xlating_fir_filter_xxx_1.set_center_freq(self.ais2_offset)

    def get_ais1_offset(self):
        return self.ais1_offset

    def set_ais1_offset(self, ais1_offset):
        self.ais1_offset = ais1_offset
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.ais1_offset)

def snipfcn_rotate_files(self):
    import os, time, threading, json


    def _write_sigmf_meta(data_path, center_freq_hz):
        meta_path = data_path.replace('.sigmf-data', '.sigmf-meta')
        now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        meta = {
            "global": {
                "core:version": "1.0.0",
                "core:datatype": "cf32_le",
                "core:sample_rate": float(self.chan_rate),
                "core:description": "AIS baseband (post freq-xlating), 200 kSps"
            },
            "captures": [
                {
                    "core:sample_start": 0,
                    "core:frequency": float(center_freq_hz),
                    "core:datetime": now_iso
                }
            ],
            "annotations": []
        }
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)


    def _rotate_files():
        os.makedirs(self.out_dir, exist_ok=True)
        while True:
            ts = time.strftime("%Y%m%d_%H%M%S")
            fname1 = os.path.join(self.out_dir, f"{self.base_name_ais1}_{ts}.sigmf-data")
            fname2 = os.path.join(self.out_dir, f"{self.base_name_ais2}_{ts}.sigmf-data")
            self.set_out_file_ais1(fname1)
            self.set_out_file_ais2(fname2)
            _write_sigmf_meta(fname1, 161975000.0)
            _write_sigmf_meta(fname2, 162025000.0)

            time.sleep(self.seg_secs)

    # start immediately
    _rotate_thread = threading.Thread(target=_rotate_files, daemon=True)
    _rotate_thread.start()


def snippets_main_after_start(tb):
    snipfcn_rotate_files(tb)




def main(top_block_cls=ais_collect_wideband, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    snippets_main_after_start(tb)
    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
