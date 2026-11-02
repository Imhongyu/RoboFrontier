# Historical snapshot: four vision-model profiles and Codex interfaces

Recorded review date: **2026-10-28**. This English edition preserves the original
research figures and source links; it does not reverify current prices, model
availability or account quotas. The [eight-provider comparison](model-compatibility-20261028.md)
includes the recorded cache write/storage and RPM/TPM/concurrency details.
Use the current [handoff guide](../multimodel-handoff.md) and frozen model catalog
for execution rather than treating a dated table as a compatibility certificate.

The original selection targeted native image understanding, function tools and
long-running agent calls. Vendor positioning was not a cross-provider accuracy
ranking; task suitability needed benchmark evidence. Figures below are regular
realtime pay-as-you-go API prices per million tokens, with uncached input in the
input column. Subscription/Coding Plan/promotional/Batch prices were excluded.

| Provider / profile | Recorded vision API model ID | Input / 1M | Output / 1M | Cache-hit input / 1M |
| --- | --- | ---: | ---: | ---: |
| Kimi / `kimi` | `kimi-k3.1-pro` | CNY 13 | CNY 68 | CNY 1.30 |
| Qwen / `qwen` | `qwen3.8-max-0902` | CNY 12 | CNY 36 | CNY 1.5 implicit; CNY 1 explicit |
| Zhipu / `glm` | `glm-5.3-flash` | CNY 0.8 | CNY 2.8 | CNY 0.23 |
| DeepSeek / `deepseek`, off-peak | `deepseek-flash` | USD 0.15 | USD 0.60 | USD 0.003 |
| DeepSeek / `deepseek`, peak | Same model | USD 0.30 | USD 1.20 | USD 0.006 |

The recorded Kimi materials positioned K3.1 Pro as its strongest flagship with
native vision. An equal-intelligence Highspeed tier listed CNY 26 input, CNY 136
output and CNY 1.30 cache-hit input. Displayed base cache writing was CNY 13/M;
ordinary input, writing and hit tokens were mutually exclusive, not two charges
for the same token. Default cache TTL was five minutes; the one-hour Pro write
price was not verified. [Model/pricing source](https://platform.kimi.com/),
[cache billing](https://platform.kimi.com/docs/guide/context-caching).

Qwen used a fixed snapshot rather than a rolling alias. The table recorded
Beijing prices; other regions could differ. The recorded Singapore tier was
CNY 14.988 input and CNY 44.965 output. Image encoding consumed input tokens.
[Vision models](https://help.aliyun.com/zh/model-studio/vision-model),
[pricing](https://help.aliyun.com/zh/model-studio/model-pricing).

Within the recorded GLM 5.3 lineup, ordinary GLM-5.3 listed text input, while
Flash/FlashX were the native multimodal series. The project selected Flash;
FlashX was a faster service tier at CNY 2 input, CNY 7 output and CNY 0.57 cache-hit
input. An extra X did not establish greater accuracy. Cache storage was listed
as temporarily free. [Flash model](https://docs.bigmodel.cn/cn/guide/models/vlm/glm-5.3-flash),
[pricing](https://docs.bigmodel.cn/cn/guide/start/pricing).

The recorded `deepseek-flash` alias referred to DeepSeek-V4.1-Flash-1017 with
vision; V4 Pro did not list vision support. Peak hours were Monday-Friday UTC
01:00-04:00 and 06:00-10:00, or Hong Kong 09:00-12:00 and 14:00-18:00, excluding
Chinese public holidays. Other times were off-peak. DeepSeek figures were USD;
the other providers' figures were CNY, without currency conversion.
[Recorded model/vision/pricing source](https://api-docs.deepseek.com/quick_start/pricing/).

Actual expense depends on request history, image encoding, cache behavior and
reasoning/output usage; four tasks do not imply a fixed bill. Preserve native
usage events and compare them with the provider's actual billing. An outer
manager session has separate usage. This dated snapshot is not a spending quote.

## Recorded native configuration mapping

| Profile | Base URL | Credential variable | Recorded native effort |
| --- | --- | --- | --- |
| `kimi` | `https://api.moonshot.cn/v1` | `KIMI_API_KEY` | `high` |
| `qwen` | Workspace/region URL from `DASHSCOPE_BASE_URL` | `DASHSCOPE_API_KEY` | `xhigh` |
| `glm` | `https://open.bigmodel.cn/api/v1` | `ZAI_API_KEY` | `max` |
| `deepseek` | `https://api.deepseek.com` | `DEEPSEEK_API_KEY` | `high` |

These were the native mappings in `configs/models.json`, using Responses.
Current unified settings may explicitly override effort; inspect the effective
configuration and generated catalog. A provider's Chat Completions support or
OpenAI-compatible format alone does not establish image input, dynamic function
tools, continuation, compaction and fork-history compatibility.

The research linked Kimi/DeepSeek Codex integration guides, Qwen's workspace/
region Responses interface and Zhipu's Responses interface, which differs from
its `/api/paas/v4` Chat endpoint. Real account/model/interface access needed a
matching preflight; no four-provider end-to-end success was claimed.
[Kimi](https://platform.kimi.com/docs/guide/codex-kimi),
[Qwen](https://help.aliyun.com/zh/model-studio/qwen-api-via-openai-responses),
[Zhipu](https://docs.bigmodel.cn/cn/guide/develop/responses/introduction),
[DeepSeek](https://api-docs.deepseek.com/quick_start/agent_integrations/codex/).

Task selection, minimum-arm cases, concurrency and offline transfer are explained
in the [handoff guide](../multimodel-handoff.md). This translation changes no model
profile, key, preflight receipt, task input or running experiment.
