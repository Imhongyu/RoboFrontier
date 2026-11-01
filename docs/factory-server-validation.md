# Factory 服务器交接验收（2026-11-01）

实现分支为 `codex/factory-server-handoff`。运行说明见 [交接文档](factory-server.md)，
数据发布为 [factory-r14-20261101](https://github.com/changxuanfan/robofrontier/releases/tag/factory-r14-20261101)。
这些检查验证数据迁移和离线渲染，不构成 benchmark 成绩或完整长片验收。

## 数据绑定

- 完整归档：5,839,108,494 bytes，分 7 卷发布；各卷大小和 SHA256 由 `configs/factory-assets.json` 固定。
- 归档 SHA256：`c713bc84b9521000b7d0b166faa409b9a368b842aaa52c9689e0e2a95c8bb3fe`。
- 数据清单 SHA256：`2d88810bc69b1104e128b72d9c1fc217a0dd0aeb195e49100ec909bfc10bda7e`。
- 完整导出、归档、另一目录恢复及 123,198 个文件的清单与校验和检查通过。
- 公开下载链接无需 GitHub 登录；Release 服务端记录的 7 卷 SHA256 与仓库配置一致。
- 36 工位保持冻结源和资格标记；Mosaic 为 R14，其中两个复用 d2 的 L3 展示仍显式保留 `recorded_case_id`。

## 本机验证

环境为 Python 3.12.6、MuJoCo 3.16.0、NumPy 2.5.4、Blender 5.1.2、FFmpeg 7.0.2；
以下视频检查显式使用 CPU。

| 检查 | 结果 | 边界 |
| --- | --- | --- |
| 工厂与证据相关自动测试 | 34 项通过 | 包括路径安全、分卷恢复、冻结计划、失败收尾和实际子进程 SIGTERM |
| 完整播放计划 | 72 项生成 | 36 工位 × front/side；没有渲染 72 条完整视频 |
| 36 工位 FK | 108 个采样状态通过 | 每桌首/中/末，最大位置误差约 5.03e-15 m；未运行物理积分 |
| 四类最小 Level 1 工位 | front/side 共 8 段通过 | 每段 3 帧，640×360、8 samples、30fps；完整解码及帧数通过 |
| 宣传片入口 | 3 帧通过 | 验证镜头/播放重启入口，不是 210.5 秒完整成片 |
| 新 benchmark motion 导入 | 四类各 1 条通过 | 真实闭合 Luna 记录及其自有冻结源；首/中/末 FK 与正面 3 帧预览通过，保留未删减剪辑 |
| 证据恢复的工厂诊断采样 | 四类通过 | 独立 MuJoCo 图像/FK 采样；不代替 Cycles 视频检查 |

自动测试命令：

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests:scripts .venv/bin/python -m unittest \
  test_factory_bundle test_factory_timeline test_factory_source_compatibility \
  test_factory_mesh_rotation test_factory_video_frames test_factory_array_replay \
  test_evidence_replay test_factory_desk_cameras test_factory_layout \
  test_factory_materials test_factory_backend
```

`test_factory_timeline` 的真实数据测试需要先 setup，否则明确跳过；不能把跳过当作通过。
本次本机执行已安装完整发布数据，没有跳过这些测试。

## Linux / Slurm

Ubuntu 22.04 计算节点通过新 clone 和服务器新建的 Python 3.12.11 环境执行。
资产准备作业 `428551` 从公开 Release 自动下载全部分卷，恢复与完整校验通过，
123,198 个文件、36 工位和清单 SHA256 均与发布匹配。
同一 CPU 分配内的验证步骤加载完整工厂和所有冻结源，36 工位 × 首/中/末共 108 个
几何状态通过，没有物理积分或模型调用。

计算节点最初缺少 `libxkbcommon.so.0`，设备检查 `428552` 和首轮视频因此失败，
首轮剩余作业已停止。补齐用户态系统库路径后，设备检查 `428561` 通过：
Blender 5.1.2、NVIDIA H800、驱动 580.159.03，OPTIX 只看到一张已分配 GPU。
这个依赖与配置方式已写入交接说明；它不是源数据或 motion 损坏。

在同一个冻结计划上重新提交数组 `428562`，8 项均 `COMPLETED / 0:0`。
四类 Level 1 最小臂数、front/side 各 3 帧、640×360、8 samples、30fps，
全部视频通过完整解码、帧数校验和带校验和的共享盘回传，生成 `complete.json`。
失败尝试保留，未被新视频覆盖；Mosaic GPU 视频已下载并目视检查。
请求并发上限为 2，但共享账号已有 7 个其他运行作业，本次实际逐项运行；
这不能用作“两张 GPU 同时渲染”的性能或并发验收。

独立 CPU 测试作业 `428565` 的上述 34 项自动测试全部通过，用时 14.023 秒、无跳过。
FFmpeg/FFprobe 使用 7.0.2-static。全部本次验证作业已结束，未更改其他人的作业。
服务器输出位于该 checkout 的 `runs/factory/linux-smoke/`，CLI status 生成视频清单；
完整验收日志位于 `runs/engineering/server-validation/`。这些运行产物不进入 Git。

尚未渲染 72 条完整工位视频或完整 210.5 秒宣传片；短测通过不代替长片验收。
