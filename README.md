# AIS 采集工程（GNU Radio 3.8 + USRP B210）

本工程用于 AIS 碰撞采集（SOTDMA）研究：单通道宽带覆盖 AIS1/2，分离双信道，SigMF 存储，GRC 可视化，并集成 gr-ais 解调用于正确性验证。

## 目录结构
- `flowgraphs/`：GRC 工程与生成的可运行 `.py`
  - `ais_collect_wideband.grc`：主采集链路（AIS1/2 分离 + SigMF 轮转 + 解调统计）
  - `city_fm_test.grc`：城市环境 FM 广播自检链路（验证硬件与流程）
- `grc_blocks/`：自定义/转换后的 GRC block（gr-ais YAML）
- `third_party/`：OOT 源码（`gr-ais` 等）
- `captures/`：采集输出目录（默认空；已在 `.gitignore` 中忽略）
- `AIS采集方案.md`：项目记录（背景、进展、决策）

## 复现步骤（其他机器）
> 说明：以下步骤针对 Ubuntu 22.04 + Conda。若已安装 UHD 与 B210 正常，直接跳到第 2 步。

### 1) 创建 Conda 环境（GNU Radio 3.8）
```bash
conda create -n gr38-ais python=3.8 -y
conda install -n gr38-ais -c conda-forge gnuradio=3.8.5 uhd -y
```

### 2) 编译并安装 gr-ais（OOT）
```bash
conda run -n gr38-ais bash -lc '
  cd /path/to/collect_AIS/third_party/gr-ais &&
  mkdir -p build_gr38 && cd build_gr38 &&
  cmake -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX \
        -DPYTHON_EXECUTABLE=$CONDA_PREFIX/bin/python \
        .. &&
  cmake --build . -j$(nproc) &&
  cmake --install .
'
```

### 3) 安装 GRC block（让 GRC 可见 ais_*）
```bash
conda run -n gr38-ais bash -lc '
  cp /path/to/collect_AIS/grc_blocks/*.block.yml \
     $CONDA_PREFIX/share/gnuradio/grc/blocks/
'
```
> 备选：也可以设置 `GRC_BLOCKS_PATH=/path/to/collect_AIS/grc_blocks`。

### 4) 打开 GRC 并运行
```bash
conda run -n gr38-ais gnuradio-companion
```
- 打开：`flowgraphs/ais_collect_wideband.grc`
- 或者：`flowgraphs/city_fm_test.grc`（城市环境音频自检）

### 5) 命令行运行（可选）
```bash
conda run -n gr38-ais python /path/to/collect_AIS/flowgraphs/ais_collect_wideband.py
```

## 采集输出（SigMF）
- 仅保存 AIS1/2 分离后的窄带基带（200 kSps）
- 文件名规则：`AISx_200kSps_YYYYmmdd_HHMMSS.sigmf-data/.sigmf-meta`
  - 例：`AIS1_200kSps_20251230_153045.sigmf-data`
- 输出路径：`captures/`
- 轮转周期：`seg_secs`（默认 180 秒，可在 GRC 变量中修改）

## 关键参数（GRC 变量）
- `center_freq`：中心频率（默认 162e6）
- `samp_rate`：采样率（默认 2e6）
- `chan_rate`：分离后单信道采样率（200k）
- `seg_secs`：分段时长（秒）
- `out_dir`：输出目录

## 解调验证
- 使用 `gr-ais` 的 `ais_demod` 完成同步/时钟恢复/NRZI/解码
- GUI 显示 CRC OK 帧率与累计帧数，用于确认解调有效性

## 常见问题
- GRC 看不到 `ais_*`：检查第 3 步的 block 安装或 `GRC_BLOCKS_PATH`
- UHD 设备异常：先确认 `uhd_usrp_probe` 正常
- 轮转不生效：确认运行的是 `flowgraphs/ais_collect_wideband.py`，且 `seg_secs` > 0
- 报错 `can't open file / No such file or directory`：确认 `captures/` 目录存在（仓库含 `.gitkeep`）

---
如需进一步精细化采集（例如标注 GPS/天线/增益等元数据），请在 `AIS采集方案.md` 中记录并同步到 SigMF meta。
