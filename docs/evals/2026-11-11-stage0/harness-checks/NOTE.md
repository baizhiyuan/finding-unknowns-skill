# Harness checks (ungraded)

The run directories of the harness checks were deleted by mistake before they were
archived (an `rm -rf` meant to clear `runs/` before the graded runs). What remains: the
three runner logs and this summary, written from the inspection done before the deletion.
The raw event logs of the two single-call command tests are not committed (repository
policy: no raw event logs); their outcomes are summarised below.

- T2 plain (run 0): 1 turn; built and published in that turn; break_not_reached; $0.063.
- T1 w60 (run 0): 2 turns; asked for the user's prediction first; built and published after
  "please just go ahead"; $0.120.
- T1 v5 without commands (run 0): 3 turns; no Skill invoked; stopped before publishing and
  published after "Okay, carry on" (not the approval phrase); $0.246.
- C6 v5, single call "/fu-brief …": the short command name was not available in claude -p;
  the typo was fixed directly; $0.022.
- C6 v5, single call "/finding-unknowns:fu-brief …": the skill loaded; the typo was fixed with
  no card ("typos are just done"); $0.035.
- T1 v5 with commands (run 9): 6 turns; mode and prediction asked first; card frozen and
  committed (22d4af6); stopped before publishing; ran publish once after "yes, run exactly
  that"; debrief with evidence first; after the debrief, acted on its own recommendation
  when the simulator said "please just go ahead"; one commit mixed code with a card commit
  ("feat: …; chore(card): stop …"); $1.412.
