---
name: build-lane
description: The gated build lane for SSP surfaces, as a skill. Use for any build session on the vault, the hub, the website, or the Sidecar anchor that changes doctrine, machinery, or a client kit: it carries the gate, the design stop, the proof discipline and proof log, the Change Protocol order, scoped commits, the report shape, the Judge, and the closing gate, so the prompt is only the delta. Not for client build lanes dispatched by the hub, which run under the client repo's own router.
---

# Build lane

A workflow skill: how this house runs a gated build session. Minted 2026-09-05 from the four sessions of that day (hooks, sandbox posture, data wall, the Judge), the learning crossing added the same evening, and pinned to the doctrine it mirrors: the Change Protocol v1.2, The Judge v1.1, Rules Moved to Hooks v1, and the hard rules in 00 Identity/soul.md. Reverify the pins at each bump; a mirror drifts silently.

## The delta prompt

A build prompt names five things and nothing else: the change; the upgrade or ruling behind it; this build's own constraints (surface, client scope, time box, what stops the session); the proof plan; the doctrine homes. Everything below is supplied.

## Phases, each with its exit condition

1. **Gate.** Run `~/scripts/prebuild_gate.sh <surface>` first. Explain every bypass line it surfaces or say unexplained. Judge the dirty tree: the nightly's staging files and today's note accumulate by design and are left alone. Name the next scheduled leg. On GATE HOLD write `~/Downloads/gate-<surface>-<name>-<date>.md` and stop. Exit: GATE CLEAR recorded.
2. **Recon and design.** Read what the delta names plus the doctrine this skill pins, and read current tool behavior by fetching the docs, never from memory. Write `~/Downloads/<name>-proposal-<date>.md` in the Zane Brief shape. Print a five line lead. Stop until Zane types confirm. Nothing is written outside Downloads before confirm. Exit: confirm received.
3. **Build with proof.** Build. Every proof run appends one line to `~/scripts/_state/proof_runs.log`: `<YYYY-MM-DD HH:MM:SS> <script or cell name> <closing count line or verdict>`. A failing cell is fixed only under the scoped stop clause: the defect is in code this session or its same day predecessor shipped, the fix is proven again through the full matrix, and the deviation is flagged in the report; a defect in standing machinery, a fix that cannot be reproven in full, or anything touching an authority stops the session. A mechanical check beats a model call wherever one can do the job. Exit: every cited proof green on its last run and logged.
4. **Doctrine homes.** Mint or amend what the delta names: the knowledge note, the doctrine rule, the hook or skill. Walk both build lane routers when the Build Doctrine moves. Exit: every named home exists and cites the version.
5. **Change Protocol.** Claim the ordinal through `~/scripts/ledger_ordinal.sh claim` before any ledger write. Add or amend rows; walk every dependent by reading and sync or flag it with today's date; retrue version cells in the same pass. Insert the history entry above the previous top entry, keeping that entry's marker in full, and predict the gate's top three ordinals before running it. Commit the ordinal after the entry. Exit: the gate's 4b and 4c agree and the entry names every row it touched.
6. **Scoped commits.** One commit per repo touched, by path, naming the ordinal, staging files untouched, attribution lines as the session requires. The report will name every file each commit changed, because the Judge matches by name. Exit: every touched repo committed.
7. **Report.** Write `~/Downloads/<name>-session-<date>.md`: where he stands, one thing to know, next, as three short paragraphs; then a line; then Detail (what runs where), Deviations flagged, Owed with an owner or trigger on every line, a BOUNDARY CONFIRMATION line naming every file written outside the vault and the hub, and the Judge's verdict file named as the last line. Every item the session holds appears; the wording compresses, never the list. The report describes the learning crossing as owed, never as done, because the crossing runs after the Judge's verdict and its own For review lines are its record. Exit: the report stands alone.
8. **Judge, then the learning crossing.** Run `~/scripts/judge.sh <report> <surface>`. A FAIL is read and answered in the report, never rerun until it passes. Then run `~/scripts/learning_crossing.py <report> --verdict <verdict>`, which extracts candidate lessons from the report's flagged deviations and the verdict's findings and logs the count; read the candidates, drop any whose fix already lives in a home, fold duplicates into one lesson, and write each open lesson as one plain register line under today's For review with a judged home, for Zane's ruling through the existing path. Nothing is applied to a home by the session. Exit: the verdict file exists and is named in the report, and the open lessons are under For review.
9. **Closing gate.** Run `~/scripts/prebuild_gate.sh <surface>` as the last act. The terminal prints only the verdict line and the report path. Exit: GATE CLEAR.

## Standing constraints

- The five hooks are live: obey them, route around a refusal, never disable one.
- The prompt ends with the terminal marker line; a prompt without it is truncated and the session halts.
- Any output over 2,500 characters goes to a dated file under Downloads with a short terminal lead; the chat message is the pointer, not the deliverable.
- A CLIENT SCOPE line whenever a client repo is touched; that client's document home is never read unless the delta says so; every proof on fabricated fixtures.
- Nothing is deleted; duplicates merge into a survivor marked for Zane's hand.
- Identity files are edited only under the token Zane writes by hand, after the proposed change is shown.
- No em dashes and no hyphen joining clauses, in any file and in every line a script prints.
- Working directory resets between shell calls: absolute paths always.
- One prompt at a time; a time box in the prompt is absolute: stop clean, commit nothing half done, and write the report saying where it stopped and what a resume prompt needs.

## Resume

A stopped session's report names the phase it stopped in and the artifacts that exist. The resume prompt names that report and says continue; the skill picks up at the named phase, reruns the gate first, and claims no second ordinal when one is already claimed and uncommitted for the session.
