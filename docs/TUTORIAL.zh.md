# 5 分钟教程

本教程面向第一次使用本插件的读者：先安装，再用真实的材料把三个技能各试一次。下面的提示词都可以直接复制。你得到的输出在措辞上会与示例不同，需要核对的是输出的*结构*。[English](TUTORIAL.md)

提示词保留英文原文，与英文版教程和录制记录一致；你也可以直接用中文提问。

## 安装（1 分钟）

在 Claude Code 会话中逐条输入：

```
/plugin marketplace add baizhiyuan/finding-unknowns-skill
```

```
/plugin install finding-unknowns@finding-unknowns-skill
```

安装后即可使用三个技能、五个子代理和三个斜杠命令（`/blindspot`、`/cartographer`、`/change-quiz`）。三个技能直接以 `/finding-unknowns`、`/keep-the-reasoning`、`/theory-vs-result` 调用，因为 Claude Code 会把技能作为斜杠命令提供。其他安装方式见 [README](../README.zh.md#快速开始)。

技能写入的文件都放在项目中的 `.finding-unknowns/` 目录下。这些是工作过程中的状态文件，默认做法是把 `.finding-unknowns/` 加入 `.gitignore`。如果要在拉取请求中审阅未知项台账和规格，请改用 [README](../README.zh.md#命令) 中的三行写法（git 无法重新纳入已被忽略目录中的文件）。

## 练习 1：在陌生仓库上做一次盲区排查（2 分钟）

目的：修改陌生代码之前，先找出你没有意识到的盲区。这里用一个小型开源库练习：

```bash
git clone https://github.com/pallets/itsdangerous.git
cd itsdangerous && git checkout 672971d   # 录制记录所用的提交
claude
```

然后在 Claude Code 中写明目标，*同时*写明你的预期（你认为答案会是什么）：

```
/blindspot I'm a grad student new to this library. I want to add secret-key rotation to
itsdangerous so our Flask app can change its SECRET_KEY without logging everyone out.
Where should I start?
Prior: I think I'll need to add a new parameter to Signer and change how signatures are
verified.
```

你应当按以下顺序得到三部分内容：

1. **与预期不符之处（Surprises）**：代码与你的预期相矛盾的地方。在这个例子中，该功能已经存在：`secret_key` 可以接收一个按从旧到新排列的密钥列表。
2. **主要发现（Top findings）**：最多三项，按影响范围排序，每项都注明 `file:line`。对于排查时看不到的内容（Flask 本身、你的应用），会标明把握程度。
3. **改写后的需求（Rewritten request）**：根据排查结果改进后的需求，可以直接作为下一条提示词。

可以与 [EXAMPLES.md 中的录制记录](../EXAMPLES.md#a-real-blind-spot-pass-recorded)（英文）对照。如果输出中没有引用位置，或者你给出了预期却没有“与预期不符之处”一节，说明运行有问题。

## 练习 2：验收改动时保留自己的判断（1 分钟）

目的：验收智能体的成果时，不在不知不觉中放弃自己的判断。练习 1 已经发现，签名器（Signer）层面本来就支持密钥轮换，而且 `test_secret_keys`（`tests/test_itsdangerous/test_signer.py:94-102`）已经覆盖了这一点：`Signer(["a", "b"])` 可以验证用 `"a"` 签名的值。但 Flask 应用是用 `URLSafeTimedSerializer` 为会话签名的，而 `test_serializer.py`、`test_timed.py` 和 `test_url_safe.py` 中没有任何测试用密钥列表构造序列化器（这些测试的夹具都只传入一个字符串密钥）。因此本练习测试的是这一层。先在虚拟环境中准备好克隆下来的仓库：

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -e . pytest freezegun   # test_timed.py 依赖 freezegun
```

然后让 Claude 做一个小改动：

```
Add a test that a URLSafeTimedSerializer token signed with secret_key="old" still loads
after the serializer is rebuilt with secret_key=["old", "new"]. Do not modify the library.
```

接着要求它给出交付报告，并说明改动要提交到哪里：

```
/keep-the-reasoning the test you just added — it goes into a PR to the shared repo
```

技能会先根据风险高低确定**交付报告大小**：`offload`（一句话）、`compact`（精简交付报告）或 `full`（完整交付报告）。决定大小的是改动的去向。只留在你自己克隆仓库中的测试，即使出错代价也很低，且只影响你本人，因此属于 `offload`。提交到共享仓库的拉取请求会影响他人，但可以撤销，并且有持续集成把关，因此属于中等风险，适用精简交付报告：先列证据，最后写结论。

```
Packet size: compact — new test in a PR to a shared library, reversible, behind CI.
Evidence           — the commands actually run and their real output
                     (e.g. `pytest tests/test_itsdangerous -q` → N passed)
What the checks did NOT prove
                   — e.g. that a real Flask session cookie survives rotation
Not checked        — at least one thing nobody verified. Never empty.
Prior vs result    — your Exercise 1 prior (a new Signer parameter would be needed)
                     against what came back (key lists already work)
Summary            — last, and short.
```

之所以出现 Prior vs result（预期与结果对照）一行，是因为练习 1 记录了预期；没有记录预期时，精简交付报告只有其余四节。请先读 What the checks did NOT prove（检查未能证明的内容）一节。如果其中声称检查已经证明了一切，就应当追问。

## 练习 3：理论与实测（1 分钟）

目的：在看到数字之前先写下预期，让数字有机会与你的预期不一致。下面是两种情形。

**（a）测量：运行之前先预测。** 技能会根据结果关系到什么来确定**严谨级别**（`note`、`report` 或 `decision`）。

```
/theory-vs-result I'm about to benchmark verify_signature with 1 key vs 3 keys in the list.
Write the prediction card first: direction, rough size, where it should show up (valid
token signed with the newest key vs an invalid token), the noise floor, and the result
that would prove me wrong. Stop before I run anything.
```

此时应当只得到一张预测卡（Claim、Mechanism chain、Prediction、Noise floor、Falsifier、Written 等字段），没有其他内容。运行之后带着数字再问一次，就会得到一张“理论预期 → 实测 → 是否一致 → 机理”卡片。

**（b）失败的测试：调试路径。** 每次都以同样方式复现的失败没有噪声下限，因此走更轻量的调试路径，而不是某个严谨级别。练习时，可以故意把练习 2 中的测试改坏：改为只用 `secret_key=["new"]` 重建序列化器（相当于过早停用了旧密钥），运行一次，然后输入：

```
/theory-vs-result the key-rotation test fails the same way on every run. Take the Debug path.
```

应当得到六项记录：复现命令及其实际输出、你的预期、至少两种相互竞争的解释、每种解释一项代价最低的检查及其结果、修复内容，以及重跑同一复现命令并加上一个不应改变的相邻用例。

## 什么时候不需要用

- **简单修改**：拼写错误、重命名，或者你已经完全理解的一行改动。
- **规格已经很详细**：需求已经具体且经过审阅时，直接实施即可。
- **没有决定依赖的数字**：一句话（“测得 X，符合预期”）就够了。

“这里没有重要的未知项”本身就是有效的结论，这些技能也会如实这样说。

## 延伸阅读

- [README](../README.zh.md)：全部功能、命令和默认值
- [术语表](GLOSSARY.md)（英文）：共用术语，包括预期（prior）、可逆性类别（lane）、严谨级别（rigor level）、交付报告大小（packet size）、模式（mode）、独立上下文反驳（fresh-context refutation）
- [架构](ARCHITECTURE.md)（英文）：命令、技能、子代理和产出文件如何配合
- [EXAMPLES.md](../EXAMPLES.md)（英文）：更多可直接复制的提示词
