# 版本沿革

finding-unknowns 怎样走到 6.0，以及怎样留在经典版本。[README](../README.zh.md#版本沿革) 只放摘要；每个版本的细节见 [CHANGELOG](../CHANGELOG.md)。英文版：[HISTORY.md](HISTORY.md)，如有出入，以英文版为准。

## 4.x：经典版本

- **内容：** 八种方法、带未知项台账的 Cartographer 模式、`keep-the-reasoning`、`theory-vs-result` 和五个子代理。
- **在哪里：** [`v4`](https://github.com/baizhiyuan/finding-unknowns-skill/tree/v4) 分支（最后发布的版本为 v4.3.2），今后只修复缺陷。
- **谁应该留下：** 使用 Cartographer、`keep-the-reasoning`、`theory-vs-result` 或子代理的人。6.0 删除了两个技能、五个子代理和三个命令。

### 怎样留在 4.x

候选版本期间什么都不会变，`main` 和插件市场提供的仍是 4.3.2。6.0.0 进入 `main` 之后：

- **新安装：** 克隆 `v4` 分支并运行其中的安装脚本。

  ```bash
  git clone -b v4 https://github.com/baizhiyuan/finding-unknowns-skill.git
  cd finding-unknowns-skill && bash install.sh
  ```

- **已有的克隆：** 用 `git checkout v4 && git pull origin v4 && bash install.sh` 更新，不要用 `git pull origin main`，否则会拉到 6.0。
- **插件：** `/plugin update` 会装上 6.0，所以不要运行它；也可以在终端里卸载插件（`claude plugin uninstall finding-unknowns@finding-unknowns-skill`），改用 `v4` 分支的克隆。

如果在 4.x 之上安装 6.0，`install.sh` 会把 6.0 删除的 4.x 组件移到 `~/.claude/finding-unknowns-backup-<时间戳>/`，`theory-vs-result` 和 `mechanism-auditor` 则原地保留。

## 5.0 至 5.2：做过设计和评测，从未发布

- **是什么：** 围绕磁盘上的任务卡组织工作，配有脚本、防护钩子和 HTML 视图。
- **怎样测的：** Stage 0 测的是重建后的 5.0（标签 `eval/stage0-v5`）；Tier 1 测的是 5.2（`v5` 分支，已归档为标签 `archive/v5.2-card`）。
- **为什么没有发布：** 打断太多，费用太高。Stage 0 中重建后的 5.0 插件得 21.0 分（满分 42），56 词版文字得 31.0 分，而插件的费用约为不做设置时的 8 倍；Tier 1 中 5.2 插件的费用约为 56 个英文词的 4.6 倍。防护钩子的 `ask` 在 `bypassPermissions` 模式下会被忽略，而作者平时正是在这个模式下工作。详见 [EVIDENCE.zh.md](EVIDENCE.zh.md#更早更短的文字)。

## 6.0：从第一性原理重新设计

- **为什么：** 作者最初的想法是把四个象限展示给人看，而在 5.x 里它们成了内部术语。5.x 的每一步都在补一个测出来的漏洞，加起来却成了围绕一个文件的记账，也没有证据表明任务卡胜过短文字。
- **留下了什么：** 测过的短文字中范围变化和不可逆操作这两个打断点（前提失效收窄为前提失效以致任务改变，预算超支这一条去掉），以及“说明每项检查没有证明什么”。
- **改了什么：** 把这张地图重新放回人的眼前，即 `fu:before` 和 `fu:after`，改动之前停一次。
- **设计与决定：** [design/6.0.md](design/6.0.md)。
