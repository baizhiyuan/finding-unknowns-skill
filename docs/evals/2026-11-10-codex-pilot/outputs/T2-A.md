建议走这条路线：**Jetson 保留 JetPack 5 系统，运行专门适配的 llama.cpp CUDA 容器，先用 1.5B 量化模型，经 Tailscale 给 home-nas 提供推理 API。Ubuntu 24.04 和 Anaconda 都不能直接解决 GPU 兼容性。**

我看了仓库，下面是结合现有结构的方案；尚未登录 Jetson，机器状态以仓库历史记录为依据。

**1. 系统：继续使用 JetPack 5**

仓库记录这台 Xavier NX 是 Ubuntu 20.04.6、5.10-tegra 内核，约 **6.7GB 可用物理内存**；已有脚本按 CUDA 11.4、`sm_72` 编译。见[硬件记录](/tmp/fu-eval/runs/T2-A/home-nas/docs/admin/现状与路线图.md:103)和[CUDA 构建脚本](/tmp/fu-eval/runs/T2-A/home-nas/nas-config/ai/build-whisper.sh:2)。

| 你的想法 | 判断 |
|---|---|
| 宿主机升级 Ubuntu 24.04 | 不建议作为部署路线。Xavier NX 官方支持仍在 JetPack 5；当前官方归档列出 5.1.8，底层仍是 Ubuntu 20.04。JetPack 6、7 的支持列表没有 Xavier。 |
| 用 Anaconda 换新 Python | 可以管理 Python 环境，但不会升级宿主机内核、GPU 驱动，也不会自动获得匹配 Jetson 的 GPU 软件包。 |
| 增加 aarch64 CUDA 容器 | 方向可行，但还必须匹配 **L4T/JetPack、CUDA、GPU 架构和推理后端**。只匹配 CPU 架构不够。 |

系统支持依据：[JetPack 官方归档](https://developer.nvidia.com/embedded/jetpack-archive)、[JetPack 5.1.8](https://developer.nvidia.com/embedded/jetpack-sdk-518)。NVIDIA 的 Jetson PyTorch 包也明确要求安装在指定 JetPack 版本上，换 Python 环境不能绕过这一点。[安装说明](https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform/index.html)

还有一个有用的余地：**JetPack 5 并非只能用 CUDA 11.4**。官方兼容表提供 CUDA 11.8～12.2 的升级路径，12.3 及以后不兼容。若所选推理版本确实需要，可单独评估升级；不能直接放进任意 CUDA 12 容器就认为可用。[CUDA for Tegra 兼容表](https://docs.nvidia.com/cuda/cuda-for-tegra-appnote/index.html#cuda-upgradable-package-for-jetson)

**2. 推理：优先 llama.cpp，小模型起步**

选 **llama.cpp + GGUF**，可以减少对 Python、PyTorch 和相关 GPU 包的依赖，也提供兼容 OpenAI 格式的 HTTP 接口及简单网页界面。[项目说明](https://github.com/ggml-org/llama.cpp/tree/master/tools/server)

建议模型顺序：

| 阶段 | 模型 | 用途 |
|---|---|---|
| 首次部署 | **Qwen2.5-1.5B-Instruct，Q4_K_M** | 验证中文问答、短文本摘要、内容分类 |
| 稳定后比较 | Qwen3-1.7B 的 GGUF 量化版本 | 比较实际效果与延迟，先采用非思考模式 |
| 后续试验 | 3B 左右的四位量化模型 | 有足够内存余量再尝试 |

Qwen2.5 首选文件约 **1.12GB**，但运行还要占用 KV cache、计算缓冲和 CUDA 内存，不能把文件大小当成总内存需求。[官方模型文件](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/tree/main)；Qwen3 也有[官方 GGUF 仓库](https://huggingface.co/Qwen/Qwen3-1.7B-GGUF)。

初始设置用 **2048 上下文、单请求并发、小 batch**。Jetson 的 CPU/GPU 共享物理内存，至少给系统留约 2GB 余量；7B 不作为这台机器的常驻目标，swap 也不能当作额外显存。[Jetson 内存架构](https://docs.nvidia.com/cuda/cuda-for-tegra-appnote/index.html#memory-management)

“较新的模型”能否运行，主要取决于**后端是否实现了模型架构、CUDA 内核是否支持 Xavier、内存是否够用**，与 Ubuntu 版本没有直接对应关系。

**3. 容器与仓库怎么放**

沿用现有平台覆盖方式：

```text
stacks/llm/
  compose.yaml
  .env.example
  README.md

platform/jetson/stacks/llm/
  compose.override.yaml
  Dockerfile
```

建议分工：

- `stacks/llm`：模型挂载、服务参数、端口、重启和日志策略。
- Jetson 覆盖层：`runtime: nvidia`、经过验证的 Jetson 镜像，以及 CUDA 构建配置。
- 模型放 Jetson 本地 NVMe，例如 `/opt/home-nas-ai/models`，以只读方式挂入容器。
- 密钥、实际镜像版本、模型路径放部署机 `.env`。

[现有 daemon 配置](/tmp/fu-eval/runs/T2-A/home-nas/platform/jetson/daemon.json:1)已经注册 NVIDIA runtime，但没有设置为默认，因此服务应显式声明。

镜像优先选择匹配宿主机 L4T 的 Jetson 基础镜像，再编译 llama.cpp，明确设置：

```text
GGML_CUDA=ON
CMAKE_CUDA_ARCHITECTURES=72
```

Xavier NX 的计算能力是 7.2；不要直接采用面向服务器 SBSA 或 Orin 的 ARM64 GPU 镜像。[NVIDIA 硬件表](https://developer.nvidia.com/cuda/gpus/legacy)

**先验证，再固定基础镜像 digest、CUDA 版本和 llama.cpp commit**。目前没有板上验证结果，不宜直接指定某个 `latest` 镜像保证可运行。

这里还有一个仓库适配点：[`bootstrap.sh`](/tmp/fu-eval/runs/T2-A/home-nas/bootstrap.sh:125)现在对所有 stack 都检查 `/mnt/nas`，而 Jetson 已经不接 NAS 数据盘。正式接入时，应增加按 stack 声明数据盘依赖的方式，让 `llm` 使用本地 NVMe；不宜长期依赖带“试跑”标记的 `--no-disk`。

**4. 给 home-nas 使用**

部署关系保持简单：

```text
home-nas（Orange Pi，100.125.87.96）
    → Tailscale
    → Jetson（100.125.87.97:8080）
    → llama.cpp → 本地模型
```

NAS 侧配置 API 基地址为 `http://100.125.87.97:8080/v1`，后续需要聊天界面时再放到 NAS 上。

端口只绑定 Jetson 的 Tailscale 地址，并配置 API key。仓库的 Tailscale 策略目前是全放行，**仅使用 Tailscale 并不等于只有 NAS 能访问**；若要限制来源，需要调整现有规则。

**5. 落地顺序与验收**

1. **核实板上环境**：L4T 包版本、CUDA、空闲内存、NVMe 空间、NVIDIA runtime；确认旧 NAS 服务是否仍占资源。
2. **验证 GPU 推理**：构建候选镜像，加载 1.5B 模型，从日志确认 GPU 层卸载，并用 `tegrastats` 查看负载和内存。
3. **接入仓库与 NAS**：完成 compose、平台覆盖、部署脚本的数据盘适配和 API 配置。
4. **验收**：测试真实中文任务、首次响应时间、生成速度、峰值内存、持续运行温度，以及重启后的恢复；同时保留镜像和模型的回滚版本。

第一版定位为**轻量文本助手**比较合适。字幕转写、翻译可以沿用仓库已有实验另做任务队列，与聊天推理错峰运行。性能和模型效果最终以这台板子的实测决定。