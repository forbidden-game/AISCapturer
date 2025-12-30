# ais_collect_wideband.grc 详细说明

本文件逐块解释 `flowgraphs/ais_collect_wideband.grc` 中的每一个模块与参数设置，帮助你理解整条采集与解调流程。

## 1. 总体流程（简述）

1) USRP 采集宽带 I/Q（中心 162 MHz，2 Msps）。
2) 通过两个 Frequency Xlating FIR 分别频移到 AIS1/2，并降采样到 200 kSps。
3) 两路信号各自写入 SigMF 文件并轮转保存。
4) 两路信号送入 gr-ais 解调 -> HDLC 解帧 -> NMEA 输出，并统计 CRC OK 帧率。
5) Qt GUI 显示宽带频谱/瀑布/时域，以及两路 AIS 频谱与解调统计。

## 2. 模块逐一说明（含参数）

### ais2_offset (`variable`)

**作用**：AIS2 相对中心频率的偏移（+25 kHz）。

**参数**：
- `comment`: ''
- `value`: 25e3

### ais_demod_rate (`variable`)

**作用**：解调链路目标采样率 = ais_sym_rate * ais_sps（应为 48 kSps）。

**参数**：
- `comment`: ''
- `value`: ais_sym_rate*ais_sps

### ais_sps (`variable`)

**作用**：解调时每个符号对应的采样点数（samples per symbol）。

**参数**：
- `comment`: ''
- `value`: '5'

### ais_sym_rate (`variable`)

**作用**：AIS 符号率（9600 bps）。

**参数**：
- `comment`: ''
- `value`: '9600'

### ant (`variable`)

**作用**：USRP 天线口选择（B210 上通常为 RX2）。

**参数**：
- `comment`: ''
- `value`: '"RX2"'

### base_name_ais1 (`variable`)

**作用**：AIS1 文件基础名（含采样率信息）。

**参数**：
- `comment`: ''
- `value`: '"AIS1_200kSps"'

### base_name_ais2 (`variable`)

**作用**：AIS2 文件基础名（含采样率信息）。

**参数**：
- `comment`: ''
- `value`: '"AIS2_200kSps"'

### center_freq (`variable`)

**作用**：USRP 中心频率（覆盖 AIS1/2 的中点）。

**参数**：
- `comment`: ''
- `value`: 162e6

### chan_bw (`variable`)

**作用**：低通滤波器通带（Hz）。

**参数**：
- `comment`: ''
- `value`: 12.5e3

### chan_rate (`variable`)

**作用**：分离后单路采样率（200 kSps）。

**参数**：
- `comment`: ''
- `value`: samp_rate/decim

### chan_trans (`variable`)

**作用**：低通滤波器过渡带（Hz）。

**参数**：
- `comment`: ''
- `value`: 5e3

### decim (`variable`)

**作用**：频移滤波后的降采样系数，输出采样率 = samp_rate/decim。

**参数**：
- `comment`: ''
- `value`: '10'

### out_dir (`variable`)

**作用**：采集输出目录。

**参数**：
- `comment`: ''
- `value`: '"/home/pan/expri/gnuradio/collect_AIS/captures"'

### out_file_ais1 (`variable`)

**作用**：AIS1 当前输出文件名（运行时会被轮转线程更新）。

**参数**：
- `comment`: ''
- `value`: out_dir + "/" + base_name_ais1 + "_" + time.strftime("%Y%m%d_%H%M%S") +

### out_file_ais2 (`variable`)

**作用**：AIS2 当前输出文件名（运行时会被轮转线程更新）。

**参数**：
- `comment`: ''
- `value`: out_dir + "/" + base_name_ais2 + "_" + time.strftime("%Y%m%d_%H%M%S") +

### resamp_decim (`variable`)

**作用**：有理数重采样的抽取因子。

**参数**：
- `comment`: ''
- `value`: '50'

### resamp_interp (`variable`)

**作用**：有理数重采样的插值因子。

**参数**：
- `comment`: ''
- `value`: '12'

### rx_gain (`variable`)

**作用**：接收增益（dB）。

**参数**：
- `comment`: ''
- `value`: '30'

### samp_rate (`variable`)

**作用**：USRP 采样率（宽带采集）。

**参数**：
- `comment`: ''
- `value`: 2e6

### samples_per_file (`variable`)

**作用**：每段理论样点数（samp_rate * seg_secs），仅作辅助显示。

**参数**：
- `comment`: ''
- `value`: int(samp_rate * seg_secs)

### seg_secs (`variable`)

**作用**：分段时长（秒）。

**参数**：
- `comment`: ''
- `value`: '10'

### xlating_taps (`variable`)

**作用**：Frequency Xlating FIR 的低通滤波器系数。

**参数**：
- `comment`: ''
- `value`: firdes.low_pass(1.0, samp_rate, chan_bw, chan_trans)

### ais_demod_0 (`ais_demod`)

**作用**：gr-ais 解调器，完成同步、频偏估计、时钟恢复、NRZI/HDLC 相关处理前端。

**关键参数说明**：
- `bits_per_sec`：符号率（9600）（当前值：ais_sym_rate）
- `samples_per_symbol`：每符号采样点数（5）（当前值：ais_sps）
- `clockrec_gain`：时钟恢复环路增益（当前值：'0.04'）
- `omega_relative_limit`：时钟恢复频偏限制（当前值：'0.01'）
- `fftlen`：频偏估计 FFT 长度（当前值：'1024'）

**参数**：
- `affinity`: ''
- `alias`: ''
- `bits_per_sec`: ais_sym_rate
- `clockrec_gain`: '0.04'
- `comment`: ''
- `fftlen`: '1024'
- `maxoutbuf`: '0'
- `minoutbuf`: '0'
- `omega_relative_limit`: '0.01'
- `samples_per_symbol`: ais_sps

### ais_demod_1 (`ais_demod`)

**作用**：gr-ais 解调器，完成同步、频偏估计、时钟恢复、NRZI/HDLC 相关处理前端。

**关键参数说明**：
- `bits_per_sec`：符号率（9600）（当前值：ais_sym_rate）
- `samples_per_symbol`：每符号采样点数（5）（当前值：ais_sps）
- `clockrec_gain`：时钟恢复环路增益（当前值：'0.04'）
- `omega_relative_limit`：时钟恢复频偏限制（当前值：'0.01'）
- `fftlen`：频偏估计 FFT 长度（当前值：'1024'）

**参数**：
- `affinity`: ''
- `alias`: ''
- `bits_per_sec`: ais_sym_rate
- `clockrec_gain`: '0.04'
- `comment`: ''
- `fftlen`: '1024'
- `maxoutbuf`: '0'
- `minoutbuf`: '0'
- `omega_relative_limit`: '0.01'
- `samples_per_symbol`: ais_sps

### ais_pdu_to_nmea_0 (`ais_pdu_to_nmea`)

**作用**：AIS PDU 转 NMEA 0183 文本输出。

**关键参数说明**：
- `designator`：信道标识符（"A"/"B"）（当前值：'"A"'）

**参数**：
- `affinity`: ''
- `alias`: ''
- `comment`: ''
- `designator`: '"A"'
- `maxoutbuf`: '0'
- `minoutbuf`: '0'

### ais_pdu_to_nmea_1 (`ais_pdu_to_nmea`)

**作用**：AIS PDU 转 NMEA 0183 文本输出。

**关键参数说明**：
- `designator`：信道标识符（"A"/"B"）（当前值：'"B"'）

**参数**：
- `affinity`: ''
- `alias`: ''
- `comment`: ''
- `designator`: '"B"'
- `maxoutbuf`: '0'
- `minoutbuf`: '0'

### blocks_file_sink_ais1 (`blocks_file_sink`)

**作用**：文件输出（SigMF 的 .sigmf-data），保存 complex64 原始样点。

**关键参数说明**：
- `file`：输出文件名变量（当前值：out_file_ais1）
- `type`：输出类型（complex64）（当前值：complex）
- `append`：是否追加写入（当前值：'False'）

**参数**：
- `affinity`: ''
- `alias`: ''
- `append`: 'False'
- `comment`: ''
- `file`: out_file_ais1
- `type`: complex
- `unbuffered`: 'False'
- `vlen`: '1'

### blocks_file_sink_ais2 (`blocks_file_sink`)

**作用**：文件输出（SigMF 的 .sigmf-data），保存 complex64 原始样点。

**关键参数说明**：
- `file`：输出文件名变量（当前值：out_file_ais2）
- `type`：输出类型（complex64）（当前值：complex）
- `append`：是否追加写入（当前值：'False'）

**参数**：
- `affinity`: ''
- `alias`: ''
- `append`: 'False'
- `comment`: ''
- `file`: out_file_ais2
- `type`: complex
- `unbuffered`: 'False'
- `vlen`: '1'

### blocks_message_debug_0 (`blocks_message_debug`)

**作用**：将 PDU/消息打印到控制台，用于现场验证解调是否有帧。

**参数**：
- `affinity`: ''
- `alias`: ''
- `comment`: ''

### blocks_message_debug_1 (`blocks_message_debug`)

**作用**：将 PDU/消息打印到控制台，用于现场验证解调是否有帧。

**参数**：
- `affinity`: ''
- `alias`: ''
- `comment`: ''

### blocks_throttle_stats_ais1 (`blocks_throttle`)

**作用**：限制 GUI 更新速率，避免统计显示占用过高 CPU。

**关键参数说明**：
- `samples_per_second`：限制输出速率（用于 GUI 数值刷新）（当前值：'2'）
- `type`：流类型（float）（当前值：float）

**参数**：
- `affinity`: ''
- `alias`: ''
- `comment`: ''
- `ignoretag`: 'True'
- `maxoutbuf`: '0'
- `minoutbuf`: '0'
- `samples_per_second`: '2'
- `type`: float
- `vlen`: '1'

### blocks_throttle_stats_ais2 (`blocks_throttle`)

**作用**：限制 GUI 更新速率，避免统计显示占用过高 CPU。

**关键参数说明**：
- `samples_per_second`：限制输出速率（用于 GUI 数值刷新）（当前值：'2'）
- `type`：流类型（float）（当前值：float）

**参数**：
- `affinity`: ''
- `alias`: ''
- `comment`: ''
- `ignoretag`: 'True'
- `maxoutbuf`: '0'
- `minoutbuf`: '0'
- `samples_per_second`: '2'
- `type`: float
- `vlen`: '1'

### digital_hdlc_deframer_bp_0 (`digital_hdlc_deframer_bp`)

**作用**：HDLC 解帧，将比特流切成 AIS 帧 PDU。

**关键参数说明**：
- `min`：最小帧长（字节）（当前值：'11'）
- `max`：最大帧长（字节）（当前值：'64'）

**参数**：
- `affinity`: ''
- `alias`: ''
- `comment`: ''
- `max`: '64'
- `maxoutbuf`: '0'
- `min`: '11'
- `minoutbuf`: '0'

### digital_hdlc_deframer_bp_1 (`digital_hdlc_deframer_bp`)

**作用**：HDLC 解帧，将比特流切成 AIS 帧 PDU。

**关键参数说明**：
- `min`：最小帧长（字节）（当前值：'11'）
- `max`：最大帧长（字节）（当前值：'64'）

**参数**：
- `affinity`: ''
- `alias`: ''
- `comment`: ''
- `max`: '64'
- `maxoutbuf`: '0'
- `min`: '11'
- `minoutbuf`: '0'

### epy_block_stats_ais1 (`epy_block`)

**作用**：自定义 Python 块（PDU 统计），输出 CRC OK FPS 等指标。

**参数**：
- `_source_code`: "\"\"\"\nEmbedded Python Blocks:\n\nEach time this file is saved,\
- `\ import gr\nimport pmt\nimport time\n\nLABEL = \"AIS1\"\n\nclass PduStats(gr.sync_block)`: \n\
- `\    \"\"\"\n    Count PDUs and report CRC OK FPS\n    \"\"\"\n    def __init__(self)`: \n\
- `\ _handle_msg(self, msg)`: \n        self._count += 1\n        self._total +=\
- `\ 1\n\n    def work(self, input_items, output_items)`: \n        now = time.time()\n\
- `\        dt = now - self._t0\n        if dt >= 1.0`: \n            if dt > 0:\n\
- `\                self._rate = self._count / dt\n            else`: \n        \
- `\        self._rate = 0.0\n            print(f\"[{LABEL}] CRC_OK_FPS={self._rate`: .2f}\
- `\ = now\n        output_items[0][`: ] = self._rate\n        return len(output_items[0])\n"
- `affinity`: ''
- `alias`: ''
- `comment`: AIS1 PDU stats
- `maxoutbuf`: '0'
- `minoutbuf`: '0'

### epy_block_stats_ais2 (`epy_block`)

**作用**：自定义 Python 块（PDU 统计），输出 CRC OK FPS 等指标。

**参数**：
- `_source_code`: "\"\"\"\nEmbedded Python Blocks:\n\nEach time this file is saved,\
- `\ import gr\nimport pmt\nimport time\n\nLABEL = \"AIS2\"\n\nclass PduStats(gr.sync_block)`: \n\
- `\    \"\"\"\n    Count PDUs and report CRC OK FPS\n    \"\"\"\n    def __init__(self)`: \n\
- `\ _handle_msg(self, msg)`: \n        self._count += 1\n        self._total +=\
- `\ 1\n\n    def work(self, input_items, output_items)`: \n        now = time.time()\n\
- `\        dt = now - self._t0\n        if dt >= 1.0`: \n            if dt > 0:\n\
- `\                self._rate = self._count / dt\n            else`: \n        \
- `\        self._rate = 0.0\n            print(f\"[{LABEL}] CRC_OK_FPS={self._rate`: .2f}\
- `\ = now\n        output_items[0][`: ] = self._rate\n        return len(output_items[0])\n"
- `affinity`: ''
- `alias`: ''
- `comment`: AIS2 PDU stats
- `maxoutbuf`: '0'
- `minoutbuf`: '0'

### freq_xlating_fir_filter_xxx_0 (`freq_xlating_fir_filter_xxx`)

**作用**：频移+低通+降采样，用于将 AIS1/2 从宽带中心频率平移到基带并抽取到目标采样率。

**关键参数说明**：
- `center_freq`：频移量（Hz，AIS1/2 偏移）（当前值：ais1_offset）
- `samp_rate`：输入采样率（当前值：samp_rate）
- `taps`：低通滤波器系数（当前值：xlating_taps）
- `decim`：降采样系数（当前值：decim）

**参数**：
- `affinity`: ''
- `alias`: ''
- `center_freq`: ais1_offset
- `comment`: ''
- `decim`: decim
- `maxoutbuf`: '0'
- `minoutbuf`: '0'
- `samp_rate`: samp_rate
- `taps`: xlating_taps
- `type`: ccf

### freq_xlating_fir_filter_xxx_1 (`freq_xlating_fir_filter_xxx`)

**作用**：频移+低通+降采样，用于将 AIS1/2 从宽带中心频率平移到基带并抽取到目标采样率。

**关键参数说明**：
- `center_freq`：频移量（Hz，AIS1/2 偏移）（当前值：ais2_offset）
- `samp_rate`：输入采样率（当前值：samp_rate）
- `taps`：低通滤波器系数（当前值：xlating_taps）
- `decim`：降采样系数（当前值：decim）

**参数**：
- `affinity`: ''
- `alias`: ''
- `center_freq`: ais2_offset
- `comment`: ''
- `decim`: decim
- `maxoutbuf`: '0'
- `minoutbuf`: '0'
- `samp_rate`: samp_rate
- `taps`: xlating_taps
- `type`: ccf

### qtgui_freq_sink_x_0 (`qtgui_freq_sink_x`)

**作用**：频谱显示（Qt GUI）。

**关键参数说明**：
- `fc`：频谱中心频率（当前值：center_freq）
- `bw`：显示带宽（当前值：samp_rate）
- `fftsize`：FFT 点数（当前值：'2048'）
- `update_time`：刷新周期（秒）（当前值：'0.10'）

**参数**：
- `affinity`: ''
- `alias`: ''
- `alpha1`: '1.0'
- `alpha10`: '1.0'
- `alpha2`: '1.0'
- `alpha3`: '1.0'
- `alpha4`: '1.0'
- `alpha5`: '1.0'
- `alpha6`: '1.0'
- `alpha7`: '1.0'
- `alpha8`: '1.0'
- `alpha9`: '1.0'
- `autoscale`: 'False'
- `average`: '1.0'
- `axislabels`: 'True'
- `bw`: samp_rate
- `color1`: '"blue"'
- `color10`: '"dark blue"'
- `color2`: '"red"'
- `color3`: '"green"'
- `color4`: '"black"'
- `color5`: '"cyan"'
- `color6`: '"magenta"'
- `color7`: '"yellow"'
- `color8`: '"dark red"'
- `color9`: '"dark green"'
- `comment`: ''
- `ctrlpanel`: 'False'
- `fc`: center_freq
- `fftsize`: '2048'
- `freqhalf`: 'True'
- `grid`: 'False'
- `gui_hint`: 0,0,1,1
- `label`: Relative Gain
- `label1`: ''
- `label10`: ''
- `label2`: ''
- `label3`: ''
- `label4`: ''
- `label5`: ''
- `label6`: ''
- `label7`: ''
- `label8`: ''
- `label9`: ''
- `legend`: 'True'
- `maxoutbuf`: '0'
- `minoutbuf`: '0'
- `name`: '"Wideband Spectrum"'
- `nconnections`: '1'
- `showports`: 'False'
- `tr_chan`: '0'
- `tr_level`: '0.0'
- `tr_mode`: qtgui.TRIG_MODE_FREE
- `tr_tag`: '""'
- `type`: complex
- `units`: dB
- `update_time`: '0.10'
- `width1`: '1'
- `width10`: '1'
- `width2`: '1'
- `width3`: '1'
- `width4`: '1'
- `width5`: '1'
- `width6`: '1'
- `width7`: '1'
- `width8`: '1'
- `width9`: '1'
- `wintype`: firdes.WIN_BLACKMAN_hARRIS
- `ymax`: '10'
- `ymin`: '-140'

### qtgui_freq_sink_x_1 (`qtgui_freq_sink_x`)

**作用**：频谱显示（Qt GUI）。

**关键参数说明**：
- `fc`：频谱中心频率（当前值：'0'）
- `bw`：显示带宽（当前值：chan_rate）
- `fftsize`：FFT 点数（当前值：'1024'）
- `update_time`：刷新周期（秒）（当前值：'0.10'）

**参数**：
- `affinity`: ''
- `alias`: ''
- `alpha1`: '1.0'
- `alpha10`: '1.0'
- `alpha2`: '1.0'
- `alpha3`: '1.0'
- `alpha4`: '1.0'
- `alpha5`: '1.0'
- `alpha6`: '1.0'
- `alpha7`: '1.0'
- `alpha8`: '1.0'
- `alpha9`: '1.0'
- `autoscale`: 'False'
- `average`: '1.0'
- `axislabels`: 'True'
- `bw`: chan_rate
- `color1`: '"blue"'
- `color10`: '"dark blue"'
- `color2`: '"red"'
- `color3`: '"green"'
- `color4`: '"black"'
- `color5`: '"cyan"'
- `color6`: '"magenta"'
- `color7`: '"yellow"'
- `color8`: '"dark red"'
- `color9`: '"dark green"'
- `comment`: ''
- `ctrlpanel`: 'False'
- `fc`: '0'
- `fftsize`: '1024'
- `freqhalf`: 'True'
- `grid`: 'False'
- `gui_hint`: 1,1,1,1
- `label`: Relative Gain
- `label1`: ''
- `label10`: ''
- `label2`: ''
- `label3`: ''
- `label4`: ''
- `label5`: ''
- `label6`: ''
- `label7`: ''
- `label8`: ''
- `label9`: ''
- `legend`: 'True'
- `maxoutbuf`: '0'
- `minoutbuf`: '0'
- `name`: '"AIS1 Spectrum"'
- `nconnections`: '1'
- `showports`: 'False'
- `tr_chan`: '0'
- `tr_level`: '0.0'
- `tr_mode`: qtgui.TRIG_MODE_FREE
- `tr_tag`: '""'
- `type`: complex
- `units`: dB
- `update_time`: '0.10'
- `width1`: '1'
- `width10`: '1'
- `width2`: '1'
- `width3`: '1'
- `width4`: '1'
- `width5`: '1'
- `width6`: '1'
- `width7`: '1'
- `width8`: '1'
- `width9`: '1'
- `wintype`: firdes.WIN_BLACKMAN_hARRIS
- `ymax`: '10'
- `ymin`: '-140'

### qtgui_freq_sink_x_2 (`qtgui_freq_sink_x`)

**作用**：频谱显示（Qt GUI）。

**关键参数说明**：
- `fc`：频谱中心频率（当前值：'0'）
- `bw`：显示带宽（当前值：chan_rate）
- `fftsize`：FFT 点数（当前值：'1024'）
- `update_time`：刷新周期（秒）（当前值：'0.10'）

**参数**：
- `affinity`: ''
- `alias`: ''
- `alpha1`: '1.0'
- `alpha10`: '1.0'
- `alpha2`: '1.0'
- `alpha3`: '1.0'
- `alpha4`: '1.0'
- `alpha5`: '1.0'
- `alpha6`: '1.0'
- `alpha7`: '1.0'
- `alpha8`: '1.0'
- `alpha9`: '1.0'
- `autoscale`: 'False'
- `average`: '1.0'
- `axislabels`: 'True'
- `bw`: chan_rate
- `color1`: '"blue"'
- `color10`: '"dark blue"'
- `color2`: '"red"'
- `color3`: '"green"'
- `color4`: '"black"'
- `color5`: '"cyan"'
- `color6`: '"magenta"'
- `color7`: '"yellow"'
- `color8`: '"dark red"'
- `color9`: '"dark green"'
- `comment`: ''
- `ctrlpanel`: 'False'
- `fc`: '0'
- `fftsize`: '1024'
- `freqhalf`: 'True'
- `grid`: 'False'
- `gui_hint`: 2,1,1,1
- `label`: Relative Gain
- `label1`: ''
- `label10`: ''
- `label2`: ''
- `label3`: ''
- `label4`: ''
- `label5`: ''
- `label6`: ''
- `label7`: ''
- `label8`: ''
- `label9`: ''
- `legend`: 'True'
- `maxoutbuf`: '0'
- `minoutbuf`: '0'
- `name`: '"AIS2 Spectrum"'
- `nconnections`: '1'
- `showports`: 'False'
- `tr_chan`: '0'
- `tr_level`: '0.0'
- `tr_mode`: qtgui.TRIG_MODE_FREE
- `tr_tag`: '""'
- `type`: complex
- `units`: dB
- `update_time`: '0.10'
- `width1`: '1'
- `width10`: '1'
- `width2`: '1'
- `width3`: '1'
- `width4`: '1'
- `width5`: '1'
- `width6`: '1'
- `width7`: '1'
- `width8`: '1'
- `width9`: '1'
- `wintype`: firdes.WIN_BLACKMAN_hARRIS
- `ymax`: '10'
- `ymin`: '-140'

### qtgui_number_sink_ais1 (`qtgui_number_sink`)

**作用**：数值显示（Qt GUI），显示统计指标。

**关键参数说明**：
- `name`：显示名称（当前值：'"AIS1 CRC OK FPS"'）
- `update_time`：刷新周期（秒）（当前值：'0.5'）

**参数**：
- `affinity`: ''
- `alias`: ''
- `autoscale`: 'True'
- `avg`: '0'
- `color1`: ("black", "black")
- `color10`: ("black", "black")
- `color2`: ("black", "black")
- `color3`: ("black", "black")
- `color4`: ("black", "black")
- `color5`: ("black", "black")
- `color6`: ("black", "black")
- `color7`: ("black", "black")
- `color8`: ("black", "black")
- `color9`: ("black", "black")
- `comment`: ''
- `factor1`: '1'
- `factor10`: '1'
- `factor2`: '1'
- `factor3`: '1'
- `factor4`: '1'
- `factor5`: '1'
- `factor6`: '1'
- `factor7`: '1'
- `factor8`: '1'
- `factor9`: '1'
- `graph_type`: qtgui.NUM_GRAPH_HORIZ
- `gui_hint`: ''
- `label1`: AIS1 CRC_OK FPS
- `label10`: ''
- `label2`: ''
- `label3`: ''
- `label4`: ''
- `label5`: ''
- `label6`: ''
- `label7`: ''
- `label8`: ''
- `label9`: ''
- `max`: '50'
- `min`: '0'
- `name`: '"AIS1 CRC OK FPS"'
- `nconnections`: '1'
- `type`: float
- `unit1`: fps
- `unit10`: ''
- `unit2`: ''
- `unit3`: ''
- `unit4`: ''
- `unit5`: ''
- `unit6`: ''
- `unit7`: ''
- `unit8`: ''
- `unit9`: ''
- `update_time`: '0.5'

### qtgui_number_sink_ais2 (`qtgui_number_sink`)

**作用**：数值显示（Qt GUI），显示统计指标。

**关键参数说明**：
- `name`：显示名称（当前值：'"AIS2 CRC OK FPS"'）
- `update_time`：刷新周期（秒）（当前值：'0.5'）

**参数**：
- `affinity`: ''
- `alias`: ''
- `autoscale`: 'True'
- `avg`: '0'
- `color1`: ("black", "black")
- `color10`: ("black", "black")
- `color2`: ("black", "black")
- `color3`: ("black", "black")
- `color4`: ("black", "black")
- `color5`: ("black", "black")
- `color6`: ("black", "black")
- `color7`: ("black", "black")
- `color8`: ("black", "black")
- `color9`: ("black", "black")
- `comment`: ''
- `factor1`: '1'
- `factor10`: '1'
- `factor2`: '1'
- `factor3`: '1'
- `factor4`: '1'
- `factor5`: '1'
- `factor6`: '1'
- `factor7`: '1'
- `factor8`: '1'
- `factor9`: '1'
- `graph_type`: qtgui.NUM_GRAPH_HORIZ
- `gui_hint`: ''
- `label1`: AIS2 CRC_OK FPS
- `label10`: ''
- `label2`: ''
- `label3`: ''
- `label4`: ''
- `label5`: ''
- `label6`: ''
- `label7`: ''
- `label8`: ''
- `label9`: ''
- `max`: '50'
- `min`: '0'
- `name`: '"AIS2 CRC OK FPS"'
- `nconnections`: '1'
- `type`: float
- `unit1`: fps
- `unit10`: ''
- `unit2`: ''
- `unit3`: ''
- `unit4`: ''
- `unit5`: ''
- `unit6`: ''
- `unit7`: ''
- `unit8`: ''
- `unit9`: ''
- `update_time`: '0.5'

### qtgui_time_sink_x_0 (`qtgui_time_sink_x`)

**作用**：时域波形显示（Qt GUI）。

**关键参数说明**：
- `srate`：时域显示采样率（当前值：samp_rate）
- `size`：显示窗口长度（当前值：'1024'）

**参数**：
- `affinity`: ''
- `alias`: ''
- `alpha1`: '1.0'
- `alpha10`: '1.0'
- `alpha2`: '1.0'
- `alpha3`: '1.0'
- `alpha4`: '1.0'
- `alpha5`: '1.0'
- `alpha6`: '1.0'
- `alpha7`: '1.0'
- `alpha8`: '1.0'
- `alpha9`: '1.0'
- `autoscale`: 'False'
- `axislabels`: 'True'
- `color1`: blue
- `color10`: dark blue
- `color2`: red
- `color3`: green
- `color4`: black
- `color5`: cyan
- `color6`: magenta
- `color7`: yellow
- `color8`: dark red
- `color9`: dark green
- `comment`: ''
- `ctrlpanel`: 'False'
- `entags`: 'True'
- `grid`: 'False'
- `gui_hint`: 1,0,1,1
- `label1`: ''
- `label10`: ''
- `label2`: ''
- `label3`: ''
- `label4`: ''
- `label5`: ''
- `label6`: ''
- `label7`: ''
- `label8`: ''
- `label9`: ''
- `legend`: 'True'
- `marker1`: '-1'
- `marker10`: '-1'
- `marker2`: '-1'
- `marker3`: '-1'
- `marker4`: '-1'
- `marker5`: '-1'
- `marker6`: '-1'
- `marker7`: '-1'
- `marker8`: '-1'
- `marker9`: '-1'
- `name`: '"Wideband Time"'
- `nconnections`: '1'
- `size`: '1024'
- `srate`: samp_rate
- `stemplot`: 'False'
- `style1`: '1'
- `style10`: '1'
- `style2`: '1'
- `style3`: '1'
- `style4`: '1'
- `style5`: '1'
- `style6`: '1'
- `style7`: '1'
- `style8`: '1'
- `style9`: '1'
- `tr_chan`: '0'
- `tr_delay`: '0'
- `tr_level`: '0.0'
- `tr_mode`: qtgui.TRIG_MODE_FREE
- `tr_slope`: qtgui.TRIG_SLOPE_POS
- `tr_tag`: '""'
- `type`: complex
- `update_time`: '0.10'
- `width1`: '1'
- `width10`: '1'
- `width2`: '1'
- `width3`: '1'
- `width4`: '1'
- `width5`: '1'
- `width6`: '1'
- `width7`: '1'
- `width8`: '1'
- `width9`: '1'
- `ylabel`: Amplitude
- `ymax`: '1'
- `ymin`: '-1'
- `yunit`: '""'

### qtgui_waterfall_sink_x_0 (`qtgui_waterfall_sink_x`)

**作用**：瀑布图显示（Qt GUI）。

**关键参数说明**：
- `fc`：瀑布中心频率（当前值：center_freq）
- `bw`：显示带宽（当前值：samp_rate）
- `fftsize`：FFT 点数（当前值：'2048'）
- `update_time`：刷新周期（秒）（当前值：'0.10'）

**参数**：
- `affinity`: ''
- `alias`: ''
- `alpha1`: '1.0'
- `alpha10`: '1.0'
- `alpha2`: '1.0'
- `alpha3`: '1.0'
- `alpha4`: '1.0'
- `alpha5`: '1.0'
- `alpha6`: '1.0'
- `alpha7`: '1.0'
- `alpha8`: '1.0'
- `alpha9`: '1.0'
- `axislabels`: 'True'
- `bw`: samp_rate
- `color1`: '0'
- `color10`: '0'
- `color2`: '0'
- `color3`: '0'
- `color4`: '0'
- `color5`: '0'
- `color6`: '0'
- `color7`: '0'
- `color8`: '0'
- `color9`: '0'
- `comment`: ''
- `fc`: center_freq
- `fftsize`: '2048'
- `freqhalf`: 'True'
- `grid`: 'False'
- `gui_hint`: 0,1,1,1
- `int_max`: '10'
- `int_min`: '-140'
- `label1`: ''
- `label10`: ''
- `label2`: ''
- `label3`: ''
- `label4`: ''
- `label5`: ''
- `label6`: ''
- `label7`: ''
- `label8`: ''
- `label9`: ''
- `legend`: 'True'
- `maxoutbuf`: '0'
- `minoutbuf`: '0'
- `name`: '"Wideband Waterfall"'
- `nconnections`: '1'
- `showports`: 'False'
- `type`: complex
- `update_time`: '0.10'
- `wintype`: firdes.WIN_BLACKMAN_hARRIS

### rational_resampler_xxx_0 (`rational_resampler_xxx`)

**作用**：有理数重采样，将 200 kSps 变为解调所需速率（48 kSps）。

**关键参数说明**：
- `interp`：插值因子（当前值：resamp_interp）
- `decim`：抽取因子（当前值：resamp_decim）
- `fbw`：设计滤波器的过渡带系数（当前值：'0.4'）

**参数**：
- `affinity`: ''
- `alias`: ''
- `comment`: ''
- `decim`: resamp_decim
- `fbw`: '0.4'
- `interp`: resamp_interp
- `maxoutbuf`: '0'
- `minoutbuf`: '0'
- `taps`: ''
- `type`: ccc

### rational_resampler_xxx_1 (`rational_resampler_xxx`)

**作用**：有理数重采样，将 200 kSps 变为解调所需速率（48 kSps）。

**关键参数说明**：
- `interp`：插值因子（当前值：resamp_interp）
- `decim`：抽取因子（当前值：resamp_decim）
- `fbw`：设计滤波器的过渡带系数（当前值：'0.4'）

**参数**：
- `affinity`: ''
- `alias`: ''
- `comment`: ''
- `decim`: resamp_decim
- `fbw`: '0.4'
- `interp`: resamp_interp
- `maxoutbuf`: '0'
- `minoutbuf`: '0'
- `taps`: ''
- `type`: ccc

### rotate_files (`snippet`)

**作用**：运行时执行的代码片段：负责文件轮转与 SigMF 元数据写入。

**关键参数说明**：
- `section`：执行时机（main_after_start）（当前值：main_after_start）
- `code`：轮转与 SigMF meta 写入逻辑（当前值："import os, time, threading, json\n\n\ndef _write_sigmf_meta(data_path,\）

**参数**：
- `alias`: ''
- `code`: "import os, time, threading, json\n\n\ndef _write_sigmf_meta(data_path,\
- `\ center_freq_hz)`: \n    meta_path = data_path.replace('.sigmf-data', '.sigmf-meta')\n\
- `\    now_iso = time.strftime(\"%Y-%m-%dT%H`: %M:%SZ\", time.gmtime())\n    meta\
- `\ = {\n        \"global\"`: {\n            \"core:version\": \"1.0.0\",\n   \
- `\         \"core`: datatype\": \"cf32_le\",\n            \"core:sample_rate\"\
- ``: float(center_freq_hz),\n                \"core:datetime\": now_iso\n     \
- `\ freq-xlating), 200 kSps\"\n        },\n        \"captures\"`: [\n         \
- `\   {\n                \"core`: sample_start\": 0,\n                \"core:frequency\"\
- `\       }\n        ],\n        \"annotations\"`: []\n    }\n    with open(meta_path,\
- `\ \"w\", encoding=\"utf-8\") as f`: \n        json.dump(meta, f, indent=2)\n\n\
- `\ndef _rotate_files()`: \n    os.makedirs(self.out_dir, exist_ok=True)\n    while\
- `\ True`: \n        ts = time.strftime(\"%Y%m%d_%H%M%S\")\n        fname1 = os.path.join(self.out_dir,\
- `comment`: Rotate capture file every seg_secs
- `priority`: '200'
- `section`: main_after_start

### uhd_usrp_source_0 (`uhd_usrp_source`)

**作用**：USRP 硬件采集源，输出复数基带 I/Q。实际生效的是通道 0（后缀 0）的参数。

**关键参数说明**：
- `center_freq0`：中心频率（通道0）（当前值：center_freq）
- `samp_rate`：采样率（当前值：samp_rate）
- `gain0`：接收增益（通道0）（当前值：rx_gain）
- `ant0`：天线口（通道0）（当前值：ant）
- `nchan`：通道数（这里为 1）（当前值：'1'）

**参数**：
- `affinity`: ''
- `alias`: ''
- `ant0`: ant
- `ant1`: RX2
- `ant10`: RX2
- `ant11`: RX2
- `ant12`: RX2
- `ant13`: RX2
- `ant14`: RX2
- `ant15`: RX2
- `ant16`: RX2
- `ant17`: RX2
- `ant18`: RX2
- `ant19`: RX2
- `ant2`: RX2
- `ant20`: RX2
- `ant21`: RX2
- `ant22`: RX2
- `ant23`: RX2
- `ant24`: RX2
- `ant25`: RX2
- `ant26`: RX2
- `ant27`: RX2
- `ant28`: RX2
- `ant29`: RX2
- `ant3`: RX2
- `ant30`: RX2
- `ant31`: RX2
- `ant4`: RX2
- `ant5`: RX2
- `ant6`: RX2
- `ant7`: RX2
- `ant8`: RX2
- `ant9`: RX2
- `bw0`: '0'
- `bw1`: '0'
- `bw10`: '0'
- `bw11`: '0'
- `bw12`: '0'
- `bw13`: '0'
- `bw14`: '0'
- `bw15`: '0'
- `bw16`: '0'
- `bw17`: '0'
- `bw18`: '0'
- `bw19`: '0'
- `bw2`: '0'
- `bw20`: '0'
- `bw21`: '0'
- `bw22`: '0'
- `bw23`: '0'
- `bw24`: '0'
- `bw25`: '0'
- `bw26`: '0'
- `bw27`: '0'
- `bw28`: '0'
- `bw29`: '0'
- `bw3`: '0'
- `bw30`: '0'
- `bw31`: '0'
- `bw4`: '0'
- `bw5`: '0'
- `bw6`: '0'
- `bw7`: '0'
- `bw8`: '0'
- `bw9`: '0'
- `center_freq0`: center_freq
- `center_freq1`: '0'
- `center_freq10`: '0'
- `center_freq11`: '0'
- `center_freq12`: '0'
- `center_freq13`: '0'
- `center_freq14`: '0'
- `center_freq15`: '0'
- `center_freq16`: '0'
- `center_freq17`: '0'
- `center_freq18`: '0'
- `center_freq19`: '0'
- `center_freq2`: '0'
- `center_freq20`: '0'
- `center_freq21`: '0'
- `center_freq22`: '0'
- `center_freq23`: '0'
- `center_freq24`: '0'
- `center_freq25`: '0'
- `center_freq26`: '0'
- `center_freq27`: '0'
- `center_freq28`: '0'
- `center_freq29`: '0'
- `center_freq3`: '0'
- `center_freq30`: '0'
- `center_freq31`: '0'
- `center_freq4`: '0'
- `center_freq5`: '0'
- `center_freq6`: '0'
- `center_freq7`: '0'
- `center_freq8`: '0'
- `center_freq9`: '0'
- `clock_rate`: '0.0'
- `clock_source0`: ''
- `clock_source1`: ''
- `clock_source2`: ''
- `clock_source3`: ''
- `clock_source4`: ''
- `clock_source5`: ''
- `clock_source6`: ''
- `clock_source7`: ''
- `comment`: ''
- `dc_offs_enb0`: '""'
- `dc_offs_enb1`: '""'
- `dc_offs_enb10`: '""'
- `dc_offs_enb11`: '""'
- `dc_offs_enb12`: '""'
- `dc_offs_enb13`: '""'
- `dc_offs_enb14`: '""'
- `dc_offs_enb15`: '""'
- `dc_offs_enb16`: '""'
- `dc_offs_enb17`: '""'
- `dc_offs_enb18`: '""'
- `dc_offs_enb19`: '""'
- `dc_offs_enb2`: '""'
- `dc_offs_enb20`: '""'
- `dc_offs_enb21`: '""'
- `dc_offs_enb22`: '""'
- `dc_offs_enb23`: '""'
- `dc_offs_enb24`: '""'
- `dc_offs_enb25`: '""'
- `dc_offs_enb26`: '""'
- `dc_offs_enb27`: '""'
- `dc_offs_enb28`: '""'
- `dc_offs_enb29`: '""'
- `dc_offs_enb3`: '""'
- `dc_offs_enb30`: '""'
- `dc_offs_enb31`: '""'
- `dc_offs_enb4`: '""'
- `dc_offs_enb5`: '""'
- `dc_offs_enb6`: '""'
- `dc_offs_enb7`: '""'
- `dc_offs_enb8`: '""'
- `dc_offs_enb9`: '""'
- `dev_addr`: '""'
- `dev_args`: '""'
- `gain0`: rx_gain
- `gain1`: '0'
- `gain10`: '0'
- `gain11`: '0'
- `gain12`: '0'
- `gain13`: '0'
- `gain14`: '0'
- `gain15`: '0'
- `gain16`: '0'
- `gain17`: '0'
- `gain18`: '0'
- `gain19`: '0'
- `gain2`: '0'
- `gain20`: '0'
- `gain21`: '0'
- `gain22`: '0'
- `gain23`: '0'
- `gain24`: '0'
- `gain25`: '0'
- `gain26`: '0'
- `gain27`: '0'
- `gain28`: '0'
- `gain29`: '0'
- `gain3`: '0'
- `gain30`: '0'
- `gain31`: '0'
- `gain4`: '0'
- `gain5`: '0'
- `gain6`: '0'
- `gain7`: '0'
- `gain8`: '0'
- `gain9`: '0'
- `iq_imbal_enb0`: '""'
- `iq_imbal_enb1`: '""'
- `iq_imbal_enb10`: '""'
- `iq_imbal_enb11`: '""'
- `iq_imbal_enb12`: '""'
- `iq_imbal_enb13`: '""'
- `iq_imbal_enb14`: '""'
- `iq_imbal_enb15`: '""'
- `iq_imbal_enb16`: '""'
- `iq_imbal_enb17`: '""'
- `iq_imbal_enb18`: '""'
- `iq_imbal_enb19`: '""'
- `iq_imbal_enb2`: '""'
- `iq_imbal_enb20`: '""'
- `iq_imbal_enb21`: '""'
- `iq_imbal_enb22`: '""'
- `iq_imbal_enb23`: '""'
- `iq_imbal_enb24`: '""'
- `iq_imbal_enb25`: '""'
- `iq_imbal_enb26`: '""'
- `iq_imbal_enb27`: '""'
- `iq_imbal_enb28`: '""'
- `iq_imbal_enb29`: '""'
- `iq_imbal_enb3`: '""'
- `iq_imbal_enb30`: '""'
- `iq_imbal_enb31`: '""'
- `iq_imbal_enb4`: '""'
- `iq_imbal_enb5`: '""'
- `iq_imbal_enb6`: '""'
- `iq_imbal_enb7`: '""'
- `iq_imbal_enb8`: '""'
- `iq_imbal_enb9`: '""'
- `lo_export0`: 'False'
- `lo_export1`: 'False'
- `lo_export10`: 'False'
- `lo_export11`: 'False'
- `lo_export12`: 'False'
- `lo_export13`: 'False'
- `lo_export14`: 'False'
- `lo_export15`: 'False'
- `lo_export16`: 'False'
- `lo_export17`: 'False'
- `lo_export18`: 'False'
- `lo_export19`: 'False'
- `lo_export2`: 'False'
- `lo_export20`: 'False'
- `lo_export21`: 'False'
- `lo_export22`: 'False'
- `lo_export23`: 'False'
- `lo_export24`: 'False'
- `lo_export25`: 'False'
- `lo_export26`: 'False'
- `lo_export27`: 'False'
- `lo_export28`: 'False'
- `lo_export29`: 'False'
- `lo_export3`: 'False'
- `lo_export30`: 'False'
- `lo_export31`: 'False'
- `lo_export4`: 'False'
- `lo_export5`: 'False'
- `lo_export6`: 'False'
- `lo_export7`: 'False'
- `lo_export8`: 'False'
- `lo_export9`: 'False'
- `lo_source0`: internal
- `lo_source1`: internal
- `lo_source10`: internal
- `lo_source11`: internal
- `lo_source12`: internal
- `lo_source13`: internal
- `lo_source14`: internal
- `lo_source15`: internal
- `lo_source16`: internal
- `lo_source17`: internal
- `lo_source18`: internal
- `lo_source19`: internal
- `lo_source2`: internal
- `lo_source20`: internal
- `lo_source21`: internal
- `lo_source22`: internal
- `lo_source23`: internal
- `lo_source24`: internal
- `lo_source25`: internal
- `lo_source26`: internal
- `lo_source27`: internal
- `lo_source28`: internal
- `lo_source29`: internal
- `lo_source3`: internal
- `lo_source30`: internal
- `lo_source31`: internal
- `lo_source4`: internal
- `lo_source5`: internal
- `lo_source6`: internal
- `lo_source7`: internal
- `lo_source8`: internal
- `lo_source9`: internal
- `maxoutbuf`: '0'
- `minoutbuf`: '0'
- `nchan`: '1'
- `norm_gain0`: 'False'
- `norm_gain1`: 'False'
- `norm_gain10`: 'False'
- `norm_gain11`: 'False'
- `norm_gain12`: 'False'
- `norm_gain13`: 'False'
- `norm_gain14`: 'False'
- `norm_gain15`: 'False'
- `norm_gain16`: 'False'
- `norm_gain17`: 'False'
- `norm_gain18`: 'False'
- `norm_gain19`: 'False'
- `norm_gain2`: 'False'
- `norm_gain20`: 'False'
- `norm_gain21`: 'False'
- `norm_gain22`: 'False'
- `norm_gain23`: 'False'
- `norm_gain24`: 'False'
- `norm_gain25`: 'False'
- `norm_gain26`: 'False'
- `norm_gain27`: 'False'
- `norm_gain28`: 'False'
- `norm_gain29`: 'False'
- `norm_gain3`: 'False'
- `norm_gain30`: 'False'
- `norm_gain31`: 'False'
- `norm_gain4`: 'False'
- `norm_gain5`: 'False'
- `norm_gain6`: 'False'
- `norm_gain7`: 'False'
- `norm_gain8`: 'False'
- `norm_gain9`: 'False'
- `num_mboards`: '1'
- `otw`: ''
- `rx_agc0`: Disabled
- `rx_agc1`: Default
- `rx_agc10`: Default
- `rx_agc11`: Default
- `rx_agc12`: Default
- `rx_agc13`: Default
- `rx_agc14`: Default
- `rx_agc15`: Default
- `rx_agc16`: Default
- `rx_agc17`: Default
- `rx_agc18`: Default
- `rx_agc19`: Default
- `rx_agc2`: Default
- `rx_agc20`: Default
- `rx_agc21`: Default
- `rx_agc22`: Default
- `rx_agc23`: Default
- `rx_agc24`: Default
- `rx_agc25`: Default
- `rx_agc26`: Default
- `rx_agc27`: Default
- `rx_agc28`: Default
- `rx_agc29`: Default
- `rx_agc3`: Default
- `rx_agc30`: Default
- `rx_agc31`: Default
- `rx_agc4`: Default
- `rx_agc5`: Default
- `rx_agc6`: Default
- `rx_agc7`: Default
- `rx_agc8`: Default
- `rx_agc9`: Default
- `samp_rate`: samp_rate
- `sd_spec0`: ''
- `sd_spec1`: ''
- `sd_spec2`: ''
- `sd_spec3`: ''
- `sd_spec4`: ''
- `sd_spec5`: ''
- `sd_spec6`: ''
- `sd_spec7`: ''
- `show_lo_controls`: 'False'
- `start_time`: '-1.0'
- `stream_args`: '""'
- `stream_chans`: '[]'
- `sync`: none
- `time_source0`: ''
- `time_source1`: ''
- `time_source2`: ''
- `time_source3`: ''
- `time_source4`: ''
- `time_source5`: ''
- `time_source6`: ''
- `time_source7`: ''
- `type`: fc32
