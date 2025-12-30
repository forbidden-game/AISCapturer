# AIS 采集方案（GNU Radio + USRP B210）

## 目标与背景
- 目标：在港口等繁忙海域采集 AIS 信号，构建数据集，用于 AIS 时域碰撞检测与恢复算法研究。
- 碰撞特性：AIS 采用 SOTDMA，固定频点（AIS1/2），繁忙海域存在同一时隙内多发射源重叠，导致接收端时频混叠与解调失败。

## 可行性结论（摘要）
- 可行：USRP B210 的带宽、双通道能力和 GNU Radio 的灵活性可以满足 AIS 原始 I/Q 采集需求。
- 关键点：需要关注动态范围、前端滤波与增益设置、时间同步与标注、数据存储量，以及现场电磁环境。

## 软件环境（当前）
- GNU Radio 3.10.1.1（Python 3.10.12）
- Ubuntu 22.04.5 LTS（jammy）

## 安装记录（gr-ais OOT 模块）
- 目标：在 GRC 内直接使用 AIS 解码模块进行现场验证。
- 现状：GNU Radio 3.10 环境不包含 SWIG 接口文件 `gnuradio.i`，导致 `gr-ais` 这类 SWIG OOT 模块无法编译完成。
- 已尝试：
  - `bistromath/gr-ais`：CMake 依赖与 SWIG 规则不兼容 GNU Radio 3.10。
  - `nauta42/gr-ais`：做了 3.10 兼容补丁（shared_ptr、Python3 语法、头文件路径等），但最终仍卡在缺失 `gnuradio.i`。
- 结论：需切换到 GNU Radio 3.8.x 的环境来完成 OOT 模块编译与 GRC 集成。

## 安装记录（gr38-ais 环境）
- conda 环境：`gr38-ais` 已创建（Python 3.8.20，GNU Radio 3.8.5.0，UHD 3.8.5.0）。
- 构建目录：`third_party/gr-ais/build_gr38`。
- CMake 配置完成（`-DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX -DPYTHON_EXECUTABLE=$CONDA_PREFIX/bin/python`）。
- 编译完成：`cmake --build third_party/gr-ais/build_gr38 -j$(nproc)`。
- 安装已完成：`cmake --install third_party/gr-ais/build_gr38` 成功写入 conda 环境。
- 兼容性补丁：由于 GRC 3.8 仅加载 `.block.yml`，`gr-ais` 自带的 `.xml` 需要转换。
  - 已生成 YAML 块文件到 `grc_blocks/`（ais_invert / ais_pdu_to_nmea / ais_square_and_fft_sync_cc）。
  - 已拷贝到 conda 环境 `share/gnuradio/grc/blocks`，现在无需再设置 `GRC_BLOCKS_PATH`。
- Flowgraph 修正：`rational_resampler` 的 `fractional_bw` 不能为 0，已改为 0.4，避免运行时报错。
- 存储方案更新：取消宽带原始 I/Q，仅保存 AIS1/AIS2 两路分离信号（200 kSps，complex64，3 分钟轮转）。
  - 已改为 SigMF：`.sigmf-data` + `.sigmf-meta`，便于后续训练/开源。
  - 文件命名包含采样率/时间：`AIS1_200kSps_YYYYmmdd_HHMMSS.sigmf-data`、`AIS2_200kSps_YYYYmmdd_HHMMSS.sigmf-data`。
- 解调链路更新：GRC 中替换为 `gr-ais` 的 `ais_demod`（包含相关同步/时钟恢复/NRZI 处理）。
- 解调统计：新增 PDU 统计块，日志输出 `CRC_OK_FPS` 与累计帧数；同时提供 QT GUI Number Sink 实时显示帧率。
- 城市环境链路自检：新增 `flowgraphs/city_fm_test.grc`（FM 广播接收 + 频谱/瀑布/音频），用于验证设备与流程。
- 轮转修复：文件轮转线程改为使用 `self.*` 属性（避免线程内 NameError 导致不轮转）。
- 修复采样率异常：`decim` 误设为 180 导致单路实际 11.1 kSps、文件过小；已恢复为 `decim=10`（单路 200 kSps）。

## 下一步计划（新会话继续）
1) 运行 GRC 时设置 `GRC_BLOCKS_PATH`（包含 `grc_blocks/`）或将生成的 `.block.yml` 复制到 conda 的 `share/gnuradio/grc/blocks`，确保 ais_* 可见。
2) 打开/检查 `flowgraphs/ais_collect_wideband.grc`，确认无 Missing Block 报错。
3) 试跑短采集验证：`blocks_message_debug` 有 AIS NMEA 输出。
4) 现场采集时根据增益/天线位置微调，确认 3 分钟分段文件正常轮转。 

## 频点与采样建议
- AIS 频点：161.975 MHz（AIS1）与 162.025 MHz（AIS2），间隔 50 kHz。
- 采集策略：
  - 单通道宽带采集：中心频率 162.000 MHz，采样率 1–2 Msps，可覆盖两信道。
  - 双通道分别采集：RX0 对 AIS1，RX1 对 AIS2；便于单独分析，但同步与校准需注意。
- 推荐采样率：2 Msps（单通道覆盖两信道，后续分离更稳健）。

## 单通道采集后的双信道分离（简易）
- GNU Radio 中使用 Frequency Xlating FIR（或 Polyphase Channelizer）即可实现，操作简单。
- 方法：以 162.000 MHz 为中心采样后，对 ±25 kHz 做频移并低通滤波，即可分离 AIS1/2。
- 优点：流程清晰、实现成本低；后处理阶段可灵活调整滤波器参数。

## 硬件与射频链路
- USRP B210（12-bit ADC，最大 56 MHz 实时带宽）：满足 AIS 25 kHz 通道与碰撞宽带采集。
- 天线：VHF 海事频段天线（160–163 MHz），尽量室外、视距良好。
- 前端滤波：建议 VHF 带通滤波，降低港口强干扰源影响。
- 动态范围：港口存在强弱信号并存，必要时加入衰减器或 LNA 组合调节。
- 设备约束：目前无 LNA，仅天线 + B210 + 笔记本；优先通过天线位置、增益设置与带通滤波优化接收。
- 同步：若有多设备协同或跨时段精确对齐需求，建议 10 MHz + PPS 或 GPSDO。

## GNU Radio 采集流程（建议）
- UHD Source：
  - 中心频率 162.000 MHz
  - 采样率 2 Msps
  - 增益：从低到高逐步调节，避免前端过载
- 频移与信道分离：
  - Frequency Xlating FIR 分离 AIS1/2
  - 低通滤波器带宽约 12.5 kHz–25 kHz
- 存储：
  - 原始 I/Q 保存为 complex64（本次选择）
  - 同时记录元数据（时间戳、增益、天线信息、位置）
  - 每 3 分钟分段保存，手动停止结束

## 现场可视化与快速验证
- 可视化：建议加入 QT GUI Frequency Sink + Waterfall + Time Sink，实时观察 AIS1/2 频点的能量与突发特征。
- 快速解码验证（可选）：
  - 分离单信道后做 GMSK 解调、时钟恢复、NRZI 反码、去比特填充、CRC 校验。
  - 仅用于确认信号正确性即可，不必追求完整高性能解码。
  - 若环境允许，也可将解码结果与已知航迹/船舶密度作粗略一致性检查。

## 开源解码器选项（用于验证）
- 建议优先使用现成开源解码器或 GNU Radio OOT 模块，不自行实现完整解码链。
- 可选路径：
  - GNU Radio OOT 模块：提供 AIS 解调/解析链路，直接在 GRC 中使用。
  - 独立 AIS 解码器：从 GNU Radio 输出的比特流/NMEA 报文接入，作为旁路验证。

## 分段存储参数（3 分钟）
- 计算公式：samples_per_file = samp_rate * 180。
- 例：2 Msps -> 360,000,000 个样本/文件。
- 文件大小（估算）：
  - complex32（8 字节/样本）约 2.88 GB/文件。
  - complex64（16 字节/样本）约 5.76 GB/文件。
- GNU Radio 实现方式（任选一种）：
  - File Meta Sink：按样本数自动分段保存。
  - Tagged File Sink：按标签分段，可配合计数器定时打标签。
  - 若版本不支持分段模块，可先整段采集，后处理按时间切分。

## 数据集组织建议
- 原始数据：按日期/地点分目录保存，命名包含频点与采样率。
- 元数据：
  - 设备信息（B210 序列号、增益设置）
  - 采集时间（UTC）
  - 地理位置（若可获取 GPS）
  - 天线与前端链路配置
- 标注与事件：建议记录现场船舶密度、气象、电磁干扰状况。

## 主要风险与对策
- 动态范围不足：调整增益、添加衰减器或改用更高动态范围 SDR。
- 前端过载：使用带通滤波器、远离强干扰源。
- 数据量大：2 Msps 复杂采样约 16 MB/s（complex32）或 32 MB/s（complex64），需准备高速存储。
- 现场条件：港口金属结构多，存在多径；可视为研究难点但也提供真实场景。

## 合规与许可
- AIS 频段为公共安全与航海通信使用，采集前需遵守当地法规。
- 不得发射干扰或非法重放信号，建议仅被动接收。

## 待确认事项
- 是否需要同时覆盖 AIS1/2 并保持严格同步？
- 是否需要绝对时间精度（PPS/GPSDO）？
- 数据集是否面向公开发布？（涉及隐私与合规）
