# PRD to Ticket to Handoff Cycle SOP

## Purpose

This SOP defines the standard process for moving product work from a PRD into phase-based tickets, completing those tickets in Cursor, producing a handoff for ACR, and feeding the results back into the PRD for the next phase. The goal is to keep Rich’s PRD as the living source of product intent while giving engineers a repeatable process for planning, execution, review, and documentation.

This SOP is optimized for AI-assisted development and is intended to operate as a **team-level operating system**, not just an individual workflow.

## Scope and Out of Scope

Use this SOP for product development work that:

- Is derived from a versioned PRD.
- Is organized into explicit phases and tickets.
- Is intended to feed implementation learnings back into the PRD via ACR.

This SOP does **not** apply to:

- Emergency hotfixes and incident response.
- Pure infrastructure work not tied to a PRD.
- Exploratory spikes and prototypes where the goal is learning, not shipping.
- Large-scale refactors or tech-debt-only sprints (these should have their own SOP or addendum).

## PRD Versioning

The PRD is a **versioned, living document**. Each PRD update must include:

- A PRD header block with:
  - **Version:** e.g. `v1.3.0`.
  - **Date:**
  - **Author:**
  - **Summary of changes:**
  - **Active phase(s):** which phases this version enables.
- A changelog entry capturing:
  - What changed.
  - Why it changed.
  - Which phases or tickets are affected.

Every phase and ticket is **pinned** to a specific PRD version:

- Phase artifacts must reference `PRD Version: vX.Y.Z`.
- Ticket descriptions must reference both the phase and PRD version they were planned against.

## When to Use

Use this SOP any time **all** of the following are true:

- There is a **versioned PRD** with an approved status.
- A phase has been **explicitly kicked off** against that PRD version (see Phase Kickoff).
- Work is being done as part of that phase’s tickets.

Do **not** use this SOP for work outside a PRD-driven phase (see Scope and Out of Scope above).

## Core Cycle

The project moves through this repeating loop:

1. **Rich creates or updates the PRD**, bumping the PRD version and updating the changelog.
2. **The PRD is broken into phases**, each with a clear goal and PRD version reference.
3. **A Phase Kickoff is created and approved** for the active phase (architect + engineering lead).
4. **Each phase is broken into tickets** with explicit ownership and dependencies.
5. **Engineers complete tickets in Cursor using a plan-first workflow.**
6. **Phase progress is tracked and updated** as tickets are completed.
7. **A Phase Delta Report is produced** comparing planned vs. actual work.
8. **A phase handoff is produced when the phase tickets are complete and stable.**
9. **The handoff goes to ACR.**
10. **ACR updates the PRD** to reflect completed work, new constraints, and next-phase direction.
11. **The architect signs off the phase**, and the cycle repeats until the product is complete.

## Governance Artifacts

### Phase Kickoff

Before any implementation begins for a phase, create a **Phase Kickoff** document (markdown or issue) that includes:

- PRD version (e.g. `PRD v1.3.0`).
- Phase name and goal.
- In-scope PRD sections.
- Out-of-scope PRD sections (for this phase).
- Known risks and constraints.
- Initial **Phase Assignment Matrix**:
  - Tickets / work items.
  - Owner for each ticket.
  - Dependencies between tickets.

The Phase Kickoff must be **approved by the architect and the engineering lead** before any tickets are started.

### Phase Delta Report

Before creating the phase handoff, produce a **Phase Delta Report** that covers:

- Planned tickets (from Phase Kickoff).
- Merged tickets (actual).
- Added work that was not originally planned (and why).
- Planned work that did not ship in this phase (and where it moved).

The delta report becomes an input to the phase handoff and a control against scope creep and under-delivery.

### ACR Operating Agreement (Interface Contract)

ACR operates against a defined contract:

- **Inputs ACR expects:**
  - Phase Kickoff reference (phase goal, PRD version).
  - Phase Delta Report.
  - Phase Handoff document.
- **Outputs ACR must produce:**
  - Updated PRD with new version header.
  - PRD changelog entry for the phase.
  - Explicit notes on unresolved questions or newly discovered risks.
- **Turnaround expectation:**
  - PRD update within an agreed SLA (e.g. 48 hours) for a completed handoff.

If ACR cannot update the PRD (blocked, missing information, disagreement), it should **reject the handoff** with explicit reasons, and the team must resolve those before proceeding.

## Roles and Ownership

- **Architect (Rich or delegate):**
  - Owns the PRD, defines intended product behavior, and sets phase-level direction.
  - Approves PRD versions and signs off on Phase Kickoff and Phase Completion.
- **Engineer:**
  - Uses Cursor to break assigned work into plans, implement tickets, document outcomes, and contribute to the phase handoff.
  - Owns ticket-level delivery and adherence to this SOP.
- **ACR:**
  - Reviews the handoff, updates the PRD, and turns completed engineering output into the next version of product direction.
  - Owns PRD consistency and changelog quality.
- **Reviewer / Tech Lead:**
  - Reviews code, confirms scope control, and checks merge readiness before completion.
  - Owns enforcement of engineering quality gates and scope compliance.
- **SOP Owner (Process Steward):**
  - Maintains this SOP, updates it based on retrospectives, and ensures new team members are onboarded to it.

## Phase Freeze Policy

- Once a phase is kicked off, **in-scope PRD sections are frozen** for the duration of that phase.
- Out-of-scope PRD sections can be updated freely.
- If an in-scope PRD change is necessary mid-phase:
  - The architect and engineering lead must update the Phase Kickoff document.
  - Engineers must acknowledge the update and adjust tickets as needed.
  - The PRD version should be bumped and referenced in updated tickets.

## Workflow

### 1. Start from the current PRD

1. Use the latest **approved and versioned** PRD from Rich as the source of truth for product scope, behavior, constraints, risks, and release intent.
2. Confirm which phase is currently active, which PRD version it is pinned to, and which tickets belong to that phase.
3. Treat the PRD as a living document that may change **between phases**, not silently in the middle of one, unless handled via the Phase Freeze Policy.

### 2. Break the active phase into engineer-readable work

1. Open the repository, the current PRD, the **Phase Kickoff document**, and any phase or assignment markdown documents in Cursor.
2. In a dedicated planning chat, ask Cursor to isolate the active phase, identify the tickets inside that phase, and separate your assigned work from the rest.
3. Review the generated task list against the PRD, the Phase Kickoff, and assignment docs before using it as your personal backlog.
4. Ensure that each ticket clearly references:
   - Phase name.
   - PRD version.
   - Owner.

**Example prompt: “Build my task list from the current PRD phase”**

```text
You are my engineering planner.

I have the current PRD, the Phase Kickoff, and phase assignment documents open.

1. Read the PRD and identify the currently active phase.
2. Within that phase, identify the tickets or work items that are assigned to me by name, role, or section.
3. Produce a numbered list of my tickets in priority order.
4. For each ticket, include:
   - A short title
   - A 2–3 sentence scope description
   - Any dependencies or prerequisites
   - A rough size tag: S, M, or L
5. At the end, add a short “Notes” section with anything that looks ambiguous, overlapping, blocked, or risky.

Do not write code. Focus only on organizing and explaining my assigned work for this phase.
```

### 3. Keep one planning chat for the phase, and one fresh chat per ticket

1. Maintain one **phase planning chat** that tracks your current ticket list and phase-level context.
2. Each time you start a new ticket, open a **new Cursor chat** for that ticket only.
3. In the ticket-specific chat, paste only the context needed for that ticket: its description, relevant PRD excerpt, Phase Kickoff snippet, and any existing handoff or spec notes.
4. Do not reuse the same implementation chat for unrelated tickets. Separate chats reduce context drift and make it easier to persist stable plans to the repository.
5. Any **non-trivial decision** made in a Cursor chat (scope change, design choice, constraint) must be written back into:
   - The mini-spec, or
   - The Phase Kickoff / Handoff document, or
   - Inline code comments,
   before the chat is considered “done.”

### 4. Plan each ticket before building it

1. In the new ticket-specific chat, ask Cursor to investigate the codebase and create an implementation plan before it writes code.
2. Require the plan to be broken into independent, reviewable subtasks.
3. Review the plan and revise it until it matches the ticket scope and phase intent.
4. **Validate the AI-generated plan** before approving it:
   - All referenced files and modules actually exist.
   - The plan does not introduce scope that isn’t in the ticket or Phase Kickoff.
   - The proposed tests actually verify the behavior described.

**Example prompt: “Break this ticket into engineering steps”**

```text
You are acting as a senior engineer helping me plan this single ticket.

Ticket description:
[paste the ticket title and scope from the phase plan]

Relevant PRD context:
[paste the most relevant PRD excerpt]

Phase context:
[paste relevant section from the Phase Kickoff]

1. Investigate the codebase and outline your implementation approach step-by-step.
2. Identify which files, modules, and systems are likely to be touched.
3. Break the work into 3–8 subtasks that can each be completed and committed independently.
4. For each subtask, give:
   - A short description
   - Expected changes, including likely files or components
   - Any tests I should add or update
5. Do not write any code yet.

Output format:
- A short “Plan” paragraph
- A numbered list of subtasks with bullets for details
```

### 5. Persist the approved ticket plan to the repo when needed

1. Create a mini-spec or handoff note for any ticket that is large, risky, cross-cutting, or likely to span multiple sessions.
2. Save it in the **canonical folder structure**, for example:
   - `docs/phases/{phase-name}/tickets/`
   - `docs/phases/{phase-name}/handoff.md`
   - `docs/prd/`
3. Use the saved file as the durable context for later implementation chats or human review.
4. If the plan changes meaningfully after initial approval, update the mini-spec so it always reflects the current intent.

**Example prompt: “Create a mini-spec file for this ticket”**

```text
I want a markdown spec file for this ticket that can be used as a handoff or reference.

Ticket:
[paste the ticket and approved subtask breakdown]

Please generate a markdown document with:
- Title
- Context (2–4 sentences)
- Goal / definition of done (bullet list)
- Subtasks (numbered list)
- Risks / open questions
- Relevant PRD references
- Phase name and PRD version

The tone should be concise and technical.
Do not include any code. Output only the markdown content.
```

### 6. Build the ticket from the approved plan

1. Stay in the ticket-specific chat once the plan is approved.
2. Implement one subtask at a time instead of asking Cursor to complete the whole ticket in one pass.
3. Review each diff before moving on.
4. Keep commits and pull requests small enough to map back clearly to the ticket and the phase.
5. If Cursor drifts, correct it directly: `You are going out of scope. Stay within Subtask N only.`

**Example prompt: “Implement this subtask”**

```text
You are my coding assistant working in this repo.

Current task: implement Subtask N from this approved ticket plan:
[paste the plan or just the relevant subtask]

Requirements:
- Keep your changes strictly within this subtask’s scope
- Prefer small, clear commits
- Add or update tests that verify the behavior described

First, briefly restate your plan for this subtask.
Then implement it step-by-step in the codebase.
Stop when this subtask is done and recap what changed.
```

### 7. Review, merge, and close the ticket work

1. Before opening a PR, pull the latest base branch, resolve conflicts locally, and confirm the changes still align with the approved ticket plan and mini-spec.
2. Ask Cursor to inspect the diff and draft the PR description.
3. Open the PR, request review, respond to comments, and merge once approved.

The **reviewer / tech lead** should apply at least this checklist:

- Does this PR map to a specific ticket and phase?
- Is the diff consistent with the approved ticket plan and mini-spec (no scope creep)?
- Are tests present and meaningful for the behavior described?
- Are there deviations from the PRD or Phase Kickoff that must be documented in the Phase Delta Report or handoff?

**Example prompt: “Generate PR description”**

```text
I am about to open a pull request for this branch.

1. Inspect the diff for this branch.
2. Generate a concise PR description with these sections:
   - Summary (2–4 sentences)
   - Changes
   - How it maps to the original ticket or mini-spec
   - Testing
   - Follow-ups
3. Use bullet points for Changes and Testing.
4. Do not invent tests that were not actually added.
5. Call out any deviations from the original ticket scope or Phase Kickoff.
6. Keep it friendly but professional.
```

### 8. Update the phase plan as tickets are completed

1. After a ticket merges, return to the **phase planning chat**.
2. Mark the completed ticket as done in the **Phase Assignment Matrix**, capture any follow-up tickets, and re-order the remaining phase work if priorities changed.
3. Keep the phase-level plan current until all tickets in the active phase are complete.

**Example prompt: “Update my phase plan based on completed ticket work”**

```text
I just merged a PR that implemented this ticket:
[paste ticket title and PR link or summary]

Here is my current phase plan:
[paste plan]

1. Mark this ticket as done.
2. If there were any follow-up items mentioned in the PR or review, add them as new tickets with appropriate priority and size.
3. Re-order the remaining tickets if needed.

Output the updated full phase plan.
```

### 9. Produce the phase delta report

Before writing the handoff:

1. Compare the Phase Kickoff (planned tickets and scope) against what actually shipped:
   - Tickets planned vs. tickets merged.
   - Extra work that was done but not originally planned.
   - Work that was planned but deferred.
2. Summarize the differences and the reasons (e.g. new discoveries, deprioritization, scope cuts).
3. Save this as a **Phase Delta Report**, and link it from the phase handoff.

### 10. Produce the phase handoff when all tickets in the phase are complete

1. Once the phase tickets are merged and **stable** (tests passing, no open regressions, reviewed by the tech lead), create a handoff document that summarizes:
   - What was built.
   - What changed relative to the PRD and Phase Kickoff.
   - What remains open.
   - What ACR needs to know to update the PRD.
2. Include implementation outcomes, deviations from the original PRD, new constraints, discovered risks, and recommended next steps for the next PRD revision.
3. Attach or link the **Phase Delta Report**.
4. Treat this handoff as the single source of truth for phase completion.

**Example prompt: “Create the phase handoff for ACR”**

```text
We have completed the tickets for this phase.

I need a markdown handoff document for ACR.

Use the Phase Kickoff, Phase Delta Report, completed ticket plans, merged PR summaries, and relevant PRD context to create a phase handoff with these sections:
- Phase name
- PRD version used for this phase
- Original phase goal from the PRD
- Tickets completed
- What was actually implemented
- Deviations from the original plan
- Risks, open questions, and technical constraints discovered during implementation
- Recommended PRD updates for the next cycle
- Suggested next-phase focus

The document should be concise, specific, and written for someone updating the PRD.
Do not include code. Output only the markdown content.
```

### 11. Hand the phase output to ACR and feed it back into the PRD

1. Send the completed phase handoff (and Phase Delta Report) to ACR.
2. ACR reviews the handoff and updates the PRD to reflect completed scope, changes in understanding, unresolved issues, and the next phase direction, then bumps the PRD version and updates the changelog.
3. The architect reviews and signs off the updated PRD and phase completion.
4. Once the updated PRD is approved, start the next cycle from the new PRD version.

## Definition of Ready

A ticket is ready to start when it has:

- A clear relationship to the current PRD phase and PRD version.
- Enough context to understand the intended outcome and acceptance criteria.
- Known dependencies or blockers captured in the Phase Assignment Matrix.
- A manageable size within the phase (S/M/L).
- An approved implementation plan before coding begins, including:
  - Identified touchpoints in the codebase.
  - Planned tests.
  - Validation that the plan matches ticket and phase scope.

## Definition of Done

A **ticket** is done when it has:

- Code implemented within the approved scope and plan.
- Relevant tests completed and passing.
- Conflicts resolved before merge.
- Reviewed pull requests merged by an assigned reviewer/tech lead.
- Any deviations from scope or PRD captured in the phase plan or mini-spec.

A **phase** is done when it has:

- All tickets in the Phase Assignment Matrix merged and stable.
- A Phase Delta Report produced (planned vs. actual).
- A phase handoff created and delivered to ACR.
- ACR has updated the PRD and bumped the PRD version.
- The architect has reviewed and signed off on phase completion.
- Any follow-up tickets or new risks logged into the backlog or next-phase plan.

## Working Rules

- Treat the PRD as the living **versioned** source of truth, and expect it to change after each handoff cycle, not silently within one.
- Keep work grouped by phase so tickets clearly map back to a specific PRD section and PRD version.
- Use one planning chat per phase, but open a **new ticket chat** every time you start a different ticket.
- Always ask Cursor to plan before asking it to build, and validate the plan before approving it.
- Persist important plans, decisions, and handoffs to the repository so later chats and reviewers can work from the same written context.
- Produce the phase handoff only after the actual merged work is stable, reviewed, and represented in the Phase Delta Report.
- Feed implementation learnings back into the PRD through ACR rather than letting the PRD drift away from reality.
- If a ticket is **blocked** for more than 24 hours, flag it in the phase plan with a written blocker description. If it remains blocked for 48 hours, escalate to the architect/tech lead for a prioritization decision.
- Treat Cursor chats as **ephemeral** context, not source of record. The repository is the source of record.
