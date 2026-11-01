# Codex / Claude harness 对齐

适用于本次代码新准备的运行；已有冻结输入和 session 不自动迁移。任务默认仍为
START 后 24 小时，工程停止时间独立设置。评分与策略进程保持独立；接受 `finish`
只是进入收尾及评分，不代表任务成功。

## 文件与职责

| 范围 | 文件 | 当前职责 |
| --- | --- | --- |
| Claude 工具编号 | `robofrontier/claude/robot_mcp.py` | 新请求生成并返回编号，同一个 MCP 请求重传保持编号；结构化返回冲突和不确定错误 |
| Claude 委派身份 | `robofrontier/claude/request_identity.py`、`fork_setup.py` | 将生成的委派编号绑定到唯一未完成的原生工具调用，再创建并核对 fork |
| Claude 策略说明 | `prompts/claude/controller.md`、`.agents/skills/robot-collaboration/references/tools.md` | 区分新请求、查询旧动作和重试不确定请求；保留显式编号兼容 |
| Claude 服务错误 | `robofrontier/claude/recovery.py`、`runner.py`、`session_host.py` | 识别结构化容量错误，保留原会话、退避和重试证据 |
| Claude 调度 | `supervisor.py`、`dispatch.py`、`adaptive_dispatch.py` | 在原截止时间内恢复；等待恢复的角色不领取普通唤醒，其他可运行角色继续 |
| 共同统计 | `robofrontier/run_metrics.py`、`scripts/export_run_report.py` | 输出统一 `host_metrics`；解析隔离的 Codex home 和收集后的 session 映射 |
| 宿主计时 | `scripts/codex_policy_host.js`、Claude 的 `runner.py`、`robot_mcp.py` | 记录轮次、工具、fork setup 耗时；不记录额外图片 Base64 |

`robofrontier/claude/` 文件仅属于 Claude 分支。共同统计、Codex 宿主计时和公共工具
说明同步到 Codex、Luna、多通信分支；各分支的启动器、模型配置和拓扑继续各自维护。

## 新请求与委派

普通新调用省略外层 `call_id`，从结果保存宿主生成的编号。查询旧动作时发起一个
新的 `job` 请求，将旧编号放在 `data.call_id`。确需重试执行结果不确定的原请求时，
使用原来的外层编号及完全相同的操作和参数；确认状态后再决定后续动作。

Claude 的 MCP JSON-RPC 请求 ID 不等于原生 `tool_use.id`。自动委派首先读取当前
Controller 的原生记录，找到参数完全相同且尚未返回的唯一工具调用；将关联写入
`private/state/claude-tool-bindings/`，然后提交委派。创建 fork 时再次校验关联。
原生记录可能稍晚写入，关联最多等待 10 秒；缺失或匹配歧义时拒绝提交，不猜测来源。
既有显式委派编号路径保留。运行中的父子原生记录和工具结果目录继续保留。

## 容量与限流恢复

仅在 CLI 已明确结束、原 session ID 匹配、结果类型为 `error_during_execution`，
且结构化错误为 `rate_limit`、`rate_limit_error`、`overloaded_error` 或
`server_overloaded` 时进入候选恢复。模型正文或 stderr 中出现“429”不算识别证据。
CLI 本身可能先重试；宿主是在其已返回失败后追加此层恢复。

恢复前核对原生记录、运行状态、停止标记、动作和委派。已接收的请求或动作仍在执行时，
先等待它们结算；动作不确定、fork 创建中、会话身份不明、停止或暂停时不自动恢复。
明确设置美元额度而费用不明的回合仍需复核。

每次连续失败最多追加 3 次恢复，退避为 10、20、40 秒；成功回合清零连续失败计数。
配置实现集中在 `recovery.py`，宿主构造参数可降低次数。等待不阻塞监督循环，也不延长
START 计时。恢复只向原 session 发送继续提示，不重新提交运动或重新创建委派；超过
次数或不满足条件时沿用停止、封存和待复核流程。取消、进程崩溃和未知结果不属于此类
安全恢复；一次工程测试也不能验证所有真实服务错误。

## 报告与统计口径

任务结束并停止所有写入后，在原来的运行环境执行：

```sh
.venv/bin/python -m scripts.export_run_report RUN_DIR
```

生成 `RUN_DIR/private/outputs/report.json`，统计位于 `host_metrics`。分析 Codex 记录时，
可用 `--codex-home PATH` 指定历史 home；否则先找收集清单的 session 映射、批次
`codex-home.json`，最后才用环境默认值。已知批次 home 不存在时不会拿其他 home 的
session 补齐。收集后的映射优先于指向原服务器的旧路径。

| 字段 | 含义与缺失处理 |
| --- | --- |
| `usage.input_tokens` | 总输入；Claude 为未缓存输入、缓存读取和缓存写入之和，Codex 输入本身包含缓存 |
| `cached_input_tokens` | 缓存读取输入；`cache_hit_rate` = 读取 / 总输入 |
| `cache_write_input_tokens` | Claude 报告的缓存写入；Codex 此接口未独立报告，值为 `null` |
| `output_tokens` | CLI / app-server 报告的输出；不额外加一次 thinking token |
| `reported_cost_usd` | 已报告费用的小计；缺失不当成零，也不自行套用价格 |
| `usage_complete`、`cost_complete` | 证据范围内字段是否齐全；未结束 CLI、损坏日志或旧版不完整证据会标记不完整 |
| `known_usage_subtotals` | 已知部分用量的小计；存在缺失回合时不能当作完整总量 |
| `by_actor`、`rows` | 角色汇总与去重后的明细；`row_unit` 区分 Claude CLI 回合和 Codex 用量更新，不能把行数直接当成相同的 API 请求数 |
| `model_process_seconds_sum` | 各回合耗时之和，包含工具等待与 CLI 开销 |
| `model_process_wall_seconds_union` | 上述时间区间并集，避免并发重复累加墙钟时间 |
| `tool_seconds_sum` | 宿主工具调用耗时之和，可能与模型进程时间重叠 |
| `fork_setup_seconds_sum` | Claude 无工具 snapshot/fork 创建回合，或 Codex 原生 fork RPC 的耗时；两种工作不同，不能据此声称条件完全相同 |

Claude 优先采用最终事件中的 `modelUsage`，汇总本轮各模型；保留 `usage` 作为后备，
两者不相加。旧记录只有回合 summary 时会标为 `legacy_policy_only`，可能缺 setup。
Codex 第一次用量更新使用 `last` 避免计入继承的父上下文，后续用累计量差分，重复更新
去重；这是宿主观测统计，不是重新计算原生转录全部历史，也不是供应商账单。
缺失字段输出 `null`，仍须检查 `usage_complete`、证据范围和原始日志。耗时含等待且
彼此重叠，不能把“模型 + 工具 + setup”相加解释为总时间占比或纯 API 延迟。

宿主日志位于 `private/outputs/codex-host.jsonl` 或 `claude-host.jsonl`；完整原生轨迹
仍由对应引擎保存及收集。新统计不会替代 session、motion、私有评分或归档验证。

## 验证与未覆盖边界

共同回归：

```sh
PYTHONPATH=tests:scripts .venv/bin/python -m unittest test_run_metrics test_run_report test_benchmark_collection test_policy_archive
node --test tests/test_codex_rpc.js tests/test_tool_errors.js tests/test_codex_wall_limit.js
```

Claude 分支另运行以下检查。物理检查需要当前 R14 资产和可用的图形环境，使用真实
Claude CLI、真实 MuJoCo 和本地合成模型服务，不使用付费服务，也不评价模型能力：

```sh
PYTHONPATH=tests:scripts .venv/bin/python -m unittest discover -s tests -p 'test_claude_*.py'
PYTHONPATH=tests:scripts ROBOFRONTIER_PHYSICS_SMOKE=1 ROBOFRONTIER_PHYSICS_BATCH=1 ROBOFRONTIER_PHYSICS_FINISH=1 ROBOFRONTIER_PHYSICS_SIGNAL=1 .venv/bin/python -m unittest test_claude_physics_smoke test_claude_parallel_physics_smoke test_claude_finish_physics_smoke test_claude_signal_physics_smoke
```

这些检查分别覆盖自动编号、真实 fork/返回、继续操作、主动结束后的独立评分，以及
墙钟/SIGTERM 停止与收集。合成模型主动 `finish` 的用例刻意未完成任务，评分必须为
未成功；它验证评分隔离，不是一次完成任务的模型成绩。真实模型完成任务、多角色
稳定性和服务端限流行为仍需另行取得授权和证据；Claude 正式计分入口继续关闭。
