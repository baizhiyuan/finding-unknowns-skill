# History

How finding-unknowns came to 6.0, and how to stay on the classic line. The
[README](../README.md#history) carries a summary; release-by-release detail is in the
[CHANGELOG](../CHANGELOG.md). Chinese: [HISTORY.zh.md](HISTORY.zh.md).

## 4.x, the classic line

- **What it is:** eight discovery techniques, Cartographer mode with its unknowns ledger,
  `keep-the-reasoning`, `theory-vs-result` and five agents.
- **Where it lives:** branch [`v4`](https://github.com/baizhiyuan/finding-unknowns-skill/tree/v4)
  (last release v4.3.2). It gets bug fixes only.
- **Who should stay on it:** anyone who uses Cartographer, `keep-the-reasoning`,
  `theory-vs-result` or the agents. 6.0 removes two skills, five agents and three commands.

### How to stay on 4.x

During the release candidate nothing changes, since `main` and the marketplace still serve
4.3.2. Once 6.0.0 is on `main`:

- **A new install:** clone branch `v4` and run its installer.

  ```bash
  git clone -b v4 https://github.com/baizhiyuan/finding-unknowns-skill.git
  cd finding-unknowns-skill && bash install.sh
  ```

- **An existing clone:** update with `git checkout v4 && git pull origin v4 && bash install.sh`,
  not `git pull origin main`, which would bring in 6.0.
- **The plugin:** `/plugin update` installs 6.0, so do not run it; or uninstall the plugin
  in your shell (`claude plugin uninstall finding-unknowns@finding-unknowns-skill`) and use
  the `v4` clone.

If you install 6.0 over 4.x, `install.sh` moves the 4.x pieces that 6.0 removed into
`~/.claude/finding-unknowns-backup-<timestamp>/` and leaves `theory-vs-result` and
`mechanism-auditor` in place.

## 5.0 to 5.2: designed and evaluated, never released

- **What they were:** the work was organised around a task card on disk, with a script, a
  guard hook and an HTML view.
- **How they were tested:** Stage 0 tested a rebuilt 5.0 (tag `eval/stage0-v5`); Tier 1
  tested 5.2 (branch `v5`, archived as tag `archive/v5.2-card`).
- **Why they were held back:** interruptions and cost. In Stage 0 the rebuilt 5.0 plugin
  scored 21.0 of 42, against 31.0 for the 56-word text, at about 8 times the cost of no setup.
  In Tier 1 the 5.2 plugin cost about 4.6 times the 56 words. The guard hook's `ask` is ignored
  under `bypassPermissions`, the mode the owner works in. Details:
  [EVIDENCE.md](EVIDENCE.md#the-earlier-shorter-texts).

## 6.0: a redesign from first principles

- **Why:** the owner's starting idea, the four quadrants shown to the person, had become
  internal vocabulary in 5.x. Each 5.x step answered a measured hole; the sum
  was bookkeeping about a file, with no evidence that the card beat the short text.
- **What it keeps:** from the measured short texts, the scope-change and irreversible-step
  stops (the falsified-premise stop narrowed to one that changes the task; the budget-overrun
  stop dropped) and "say what each check did not prove".
- **What it changes:** it puts the map back in front of the person, as `fu:before` and
  `fu:after`, with one pause before changes.
- **Design and decisions:** [design/6.0.md](design/6.0.md).
