# Factory Linux / Slurm 交接

本入口读取冻结的 motion、外观事件和剪辑，做 FK 和 Blender Cycles 离线渲染。
没有模型调用、机器人命令、接触仿真或新的任务成绩。真实 benchmark 的 Slurm/SQLite
存储限制仍见 `server-benchmark.md`，不能用本渲染入口的验收替代。

## 安装与数据

从本分支 clone 后，在仓库根安装锁定的 Python 3.12 依赖：

```sh
uv sync --locked
```

另需 Blender 5.1.2、FFmpeg 和 FFprobe，三者应在计算节点可执行。设置
`BLENDER_BIN=/绝对路径/blender`；FFmpeg/FFprobe 放到 PATH。Linux NVIDIA GPU
用 OPTIX，显式 CUDA 可作为另一选项；Mac 用 METAL，CPU 仅供显式诊断。
缺少指定 GPU 后端时失败，不会静默切换 CPU。本仓库不分发集群驱动或复制其他机器的 `.venv`。

```sh
.venv/bin/python -m scripts.factory_server setup
```

默认安装到 `runs/factory-data/r14/`。`configs/factory-assets.json` 固定 Release、
分卷 SHA256、完整归档 SHA256 和数据清单 SHA256；自动依次下载分卷、拼接、验证和
恢复，无须手动找到 Release。离线已有完整归档时加 `--archive /path/factory.tar.gz`。
自选数据目录用 `--data-root /shared/path/factory-r14`，后续命令也传相同目录。
使用绝对路径方便排队作业；数据目录不要安装在有小额配额的 home。

数据包包括 36 工位、Mosaic R14、各录制自己的冻结场景/资产、motion、事件、剪辑
及其语义校验证据、相机和预导出的 Blender 场景。与约 186 MB 的 benchmark 场景
包不同，这是完整历史播放数据，下载约 5.84 GB，解压逻辑大小约 9.8 GB；硬链接会
减少实际占用。首次准备应留至少 20 GB 可用空间，下载期间还需暂存归档。
运行和渲染中间帧另需空间，大小随时长和分辨率增长。不要把数据包提供给策略模型作为任务输入。

新包与 `policy-assets.json` 分开，未修改现有 benchmark 资产清单或物理定义。
历史录制保持其实际源物理；离线渲染不把旧轨迹冒充为新摩擦参数下重新执行。
Mosaic 的 a06-d3、a08-d3 展示复用对应 d2 记录，并保留 `recorded_case_id` 和物理
等价检查；它们不是新增的 Level 3 运行或成功证明。其他来源的资格标记也原样保留。

## 先做短测

在有 GPU 的计算环境检查软件和所选设备：

```sh
.venv/bin/python -m scripts.factory_server doctor --device OPTIX
```

登录节点没有 GPU 时，不能用其检查结果推断计算节点 GPU 可用；可先用 `--device CPU`
检查 CPU 路径，再通过下述短作业验证 GPU。doctor 不产生视频、不调用模型。

下面选择四类的 Level 1 最小臂数、front/side，共 8 个一秒预览。
默认正式画质为 1920×1080、30fps、64 samples；此短测降低尺寸和采样以检查交接。

```sh
.venv/bin/python -m scripts.factory_server prepare \
  --output runs/factory/smoke \
  --cases transport-a04-d1 mosaic-a04-6x12-d1 relay-a08-d1 dial-best5-n04-d1 \
  --duration-s 1 --width 640 --height 360 --samples 8 --device OPTIX

.venv/bin/python -m scripts.factory_server submit \
  --plan runs/factory/smoke/plan.json --partition YOUR_PARTITION \
  --parallel 2 --cpus 20 --memory 64G --time 01:00:00 --dry-run
```

核对生成的 sbatch 参数后，去掉 `--dry-run` 提交。资源和分区由所在集群决定，
示例不保证即时获得 GPU。某些集群先加载 Slurm 模块；本组当前环境为：

```sh
module load slurm/slurm/23.02.6
```

提交命令自动创建作业数组，一项占一张 GPU；`--parallel` 控制同时运行的渲染项数，
不是模型并发数。提交目录应是共享、计算节点可访问的 checkout，Python 环境、数据
和 BLENDER_BIN 也须可访问。模板不包含个人账号或固定 Lustre 路径。
Slurm 时限涵盖准备、渲染、编码和回传，和 benchmark 的 START 时限无关。

## 完整工位视频与宣传片

省略 `--duration-s` 渲染完整剪辑。未指定筛选时 36 工位 × 两相机，共 72 项：

```sh
.venv/bin/python -m scripts.factory_server prepare \
  --output runs/factory/full --device OPTIX
.venv/bin/python -m scripts.factory_server submit \
  --plan runs/factory/full/plan.json --partition YOUR_PARTITION --parallel 2
```

可用 `--families transport relay`、`--levels 1 2`、`--views front` 缩小范围，或通过
`--cases 任务ID ...` 精确选择。准备阶段校验完整数据包；每个渲染项重新校验它会使用的
源记录、场景、资产和相机，避免每项都重新读取其他任务的大型历史记录。
普通桌面模式按源剪辑独立播放；相机固定，源状态和外观事件不被重新求解。

宣传片是一个独立作业，默认 210.5 秒，使用全工厂镜头和显式记录的工位播放重启：

```sh
.venv/bin/python -m scripts.factory_server prepare \
  --output runs/factory/promo --mode promo --device OPTIX
.venv/bin/python -m scripts.factory_server submit \
  --plan runs/factory/promo/plan.json --partition YOUR_PARTITION --parallel 1
```

宣传片中的 `reset-events.json`、逐帧来源和相机计划保留。这是展示剪辑，不是一次
从头到尾同步执行的多任务实验。

## 本机执行和结果

本机准备时选 `--device METAL`，CPU 诊断选 `--device CPU`。不需要 Slurm：

```sh
.venv/bin/python -m scripts.factory_server run --plan runs/factory/local/plan.json --index 0
.venv/bin/python -m scripts.factory_server status --plan runs/factory/local/plan.json
```

`local` 是先用 prepare 创建的批次；每次 prepare 都要选择新输出目录。数据可以搬迁
后重新 prepare；已经准备的计划绑定该机器的输入位置和源码哈希，不可直接修改计划。
更改渲染代码或参数后重新 prepare；旧批次和旧结果保留。

```text
批次/
├── plan.json、plan.sha256、release.json
├── logs/                         Slurm 日志
├── jobs/工位--相机/
│   ├── complete.json             只在视频验证及回传成功后生成
│   └── attempt-唯一编号/
│       ├── poses/                源状态映射、相机、姿态
│       ├── render/factory.mp4
│       ├── render/report.json
│       ├── render.log
│       └── attempt.json
└── summary.json                  status 命令生成，含视频地址
```

脚本在 SLURM_TMPDIR、TMPDIR 或 `/tmp` 中渲染，结束后校验复制回批次目录。
此流程没有活跃 SQLite。Slurm 终止前预留 180 秒发送信号并尝试收尾；SIGKILL、
节点丢失或回传失败可能留下未封存尝试，此时保留日志中的本地路径，不能标记成功。
节点本地空间和集群清理策略仍由站点决定，作业资源需留足收尾时间。

MP4 完整解码、帧数/30fps 检查通过后才删除渲染中间 PNG；失败保留已有帧。
不会删除 source 纹理 PNG、motion 或模型观察 JPG。报告中的原始临时路径作为来源
记录保留，分析时以本批次实际文件和 complete.json 为准。

重新运行同一 index 会验证已完成视频并跳过；失败或中断会使用新的 attempt 目录。
不会覆盖旧视频、自动恢复半个 Blender 进程或混用不同计划。使用 status 确认哪些
项目需要补跑；集群作业是否排队/运行仍以 squeue/sacct 为准。

## 渲染新的 benchmark motion

等待原任务所有写入停止，使用其 `private/outputs/motion/`，不是图片目录或 session：

```sh
.venv/bin/python -m scripts.factory_server import-motion \
  --recording /path/to/run/private/outputs/motion \
  --output runs/factory-data/my-recording --speedup 1
.venv/bin/python -m scripts.factory_server prepare \
  --data-root runs/factory-data/my-recording \
  --output runs/factory/my-recording --device OPTIX
```

支持本发布 36 个任务 ID；Mosaic 显示源仍须是 R14。程序用该记录自己的冻结
source 重建对应工位，并导出新的 Blender 场景；其他工位是静态背景。保留完整
motion 和外观事件，生成全保留剪辑，不猜测任务成功、不套用 Oracle 的完成前缀。
缺少源资产、记录仍活跃、任务不匹配或运动校验失败时拒绝导入。
旧 motion 格式由现有 MotionReader 读取；压缩归档请先用对应恢复命令还原目录。

## 维护者发布

`export` 从显式 scene/release/cameras/asset/source-root 生成可迁移数据目录；
`pack` 验证所有文件并输出 tar.gz。分发包保留编辑与运动的原始字节，内容相同的
文件使用硬链接去重。分卷清单由 `factory_bundle.split_archive` 生成，发布后固定在
`configs/factory-assets.json`。更新包使用新文件名和哈希，保留旧发布供历史复现。
不要改 benchmark 的 current.json 来切换 factory 数据。

压缩证据验收的 factory 选项使用独立的 MuJoCo 采样图/FK 检查，生产视频继续使用
Cycles；两者都不运行物理。采样图通过不等于完整视频或任务评分通过。
