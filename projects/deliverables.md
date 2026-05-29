# Project Deliverables & Sprint Rules

*AI Design course. Applies to all projects (ideas 1–6). Team size: **2 to 4 students**. Weekly sprints. What happens **inside** each sprint is decided as we go — in the project meetings. The deliverables and the sprint rules below are constant.*

*This doc applies to students attending lessons regularly. A separate policy covers students unable to attend (TBD).*

---

## 1. What every project ships

Five things at the end. Everything else is optional polish.

1. **Working code with a UI** — a git repo with a runnable system that someone else can clone, start, and actually interact with. CLI, notebook, web app, desktop — whatever fits the project. README, dependency file, seed control, config-driven experimental conditions. "Working" and "usable by a human other than you" are the bar.
2. **Project-specific data artifacts** — whatever data, models, logs, or graphs your project produces (persona JSONs, cluster-refinement traces, synthetic datasets, KB snapshots, extracted graphs, rater responses, behavior logs, etc.). Versioned; runs replayable from what's in the repo.
3. **Findings** — concrete, specific, defensible things you discovered about agent behaviors. *This is the point of the project.* Not "we built a system and it works" — but specific observations: *"persona X dominates group chats," "the KB converges after ~N edits," "agents given tool Y persist 3× longer at failing tasks," "conversational refinement does NOT improve silhouette on this dataset."* Surprises, failures, and unexpected behaviors count as findings too — arguably the most interesting kind.
4. **Technical report** — research-paper-style writeup: intro, (related work if study-heavy, see below), method, experiments, results with confidence intervals, findings, discussion, limitations, ethics. A *well-executed null result* counts as success.
5. **Final presentation** — slide deck telling the story end-to-end (20 min for groups of up to 3, 30 min for groups of 4–5): question → method → **findings** → limitations → **contributions of each team member**. See the projects page for what to cover.

The universal scaffolding (`universal_scaffolding.md`, 13 components) is assumed throughout. These five sit on top of that infrastructure and fail to exist without it.

---

## 2. Build-heavy vs Study-heavy

Every project **builds** something and **studies** something. The balance shifts project to project, and it shapes what we expect.

**Build-heavy projects.** The contribution is the system. Most of the effort is engineering: a richer UI, more features, handling edge cases, scaling up. The findings come from observing what the built system does. The elevated expectation is on the build itself — polished UI, wider feature set, robustness, clean handoff so another team could extend it. The findings section can be shorter because the system is doing more of the talking.

**Study-heavy projects.** The contribution is the study. The build is minimum-viable — just enough to enable the experiment. Most of the effort goes into designing how to probe the agents, reading prior work, running the experiment carefully, analyzing results, and writing them up rigorously. Study-heavy projects add **two things** to the deliverables above:

- A **short state-of-the-art / related-work section** embedded in the report, surveying how others have studied similar phenomena. Not exhaustive — just enough to position your methodology and motivate the design choices.
- An explicit **study-design plan**: how you'll probe the agents, what conditions, what you measure, why this design and not another. Committed early in the project and referred back to in the final report.

**Mixed projects.** Roughly balanced between the two. The report gives equal weight to the system and the study.

Teams declare their profile in the proposal. The grader's lens adjusts accordingly — a build-heavy team is evaluated primarily on the system and its findings; a study-heavy team primarily on the study design, state-of-the-art awareness, and depth of analysis.

*Example leanings* (not prescriptions — teams can push either way with justification):

- Conversational Clustering — typically build-heavy
- WhatsApp Personas — mixed

---

## 3. Sprint rules

**At the start of each sprint:**

- Every team member has **one clearly-defined job** for the week. Written down. Owned. Not "we'll figure it out as we go."

**At the end of each sprint, we want to see:**

- **Commits from each person, under their own name, in the repo.** "We worked from the same computer" is not a thing in this course. If it's your job, your commits reflect you doing it. Pair-programming is fine — the commit history still shows individual contributions.
- **Results.** Whatever your job was supposed to produce — code, data, analysis, writing — shows concrete output. No "I thought about it a lot."
- **A one-slide-per-person report.** Brief. Three things: *what I did this sprint, what blocked me, what I'm doing next.* Presented live in the next lesson.
- **The same report in markdown**, committed to the repo at `/notes/sprint-<N>-<yourname>.md`. The slide is for the meeting; the markdown is the audit trail.

**Lessons are project meetings.** We use class time to discuss each project together — progress, decisions, open problems, stuck points. Come prepared to present your slide and defend your work.

**You own your commits.** Fabio and graders can ask you, specifically, about any commit under your name. "My teammate wrote that" is not an answer. If it's yours, you understand it; if it's theirs, it's in their history, not yours.

**Tracking.** All work happens in the project's git repo on GitHub. The process:

- **One issue per person per sprint.** Filed at sprint start, describing that person's job for the week. Assigned to themselves. Closed at sprint end by a commit or PR that references it (e.g., `Closes #7` in the commit message).
- **One milestone per sprint.** Issues attach to the current sprint's milestone. This gives a built-in "what got done vs. what's left" view at each sprint boundary.
- **Sprint-end markdown note (`/notes/sprint-<N>-<yourname>.md`) stays.** Issues track the *job*; the markdown note is the *narrative*. Different artifact, different purpose.

Optional, not required: Pull Requests (direct-to-main is fine for solo work; PRs welcome if the team wants code-review practice), GitHub Projects kanban board (useful for teams of 4, overhead for teams of 2), GitHub Actions / CI (nice if you want it; not expected in a 4-week window).

---

## 4. Assessment

We grade on the end deliverables **and** on how you got there. Process is not neutral — a beautiful report produced by one person while the others coasted is not a team that earned a team grade.

**What we look at:**

- **Consistency across sprints.** Real work visible every week, not last-minute crams. A team that produces half the output four weeks in a row beats a team that produces nothing for three weeks and a miracle in the fourth.
- **Individual accountability.** Commits under each person's name, spread across sprints. Each person can defend their commits in a project meeting — *"my teammate wrote that"* is not an answer.
- **Engineering quality.** Clean APIs between modules; sensible modularization; prompts as versioned files, not embedded f-strings; structured logging on every run; errors fail loudly rather than hide. The minimum-acceptable bars from `universal_scaffolding.md` are the floor, not the goal.
- **Observability.** Every run leaves a trace. You can replay it. Errors don't hide. A grader can open the logs and understand what happened without you in the room.
- **Reproducibility.** Fresh clone → documented command → headline result reproduces. This is the single cheapest signal of engineering seriousness.
- **Working system and UI.** The code runs on a machine that isn't yours. The UI is usable by a stranger without a 20-minute onboarding.
- **Findings quality.** Specific, defensible, interesting observations about agent behavior — not "we built a system and it works." Could a peer ask *"how do you know that?"* and get a concrete, quantified answer?
- **Experimental honesty.** Uncertainty is quantified (confidence intervals, ranges, error bars — not just point estimates). Negative or surprising findings are reported, not buried. Deviations from the initial plan are explained, not hidden.
- **Scope discipline.** Ambition matched to team size and the four sprints available. Cutting scope early is a positive signal; finishing at 60% because you overreached is a negative one.
- **Communication.** The report and presentation tell the story — question → method → findings → limitations — clearly enough that a peer gets the idea in ten minutes.

**For study-heavy projects, additionally:**

- **Awareness of prior work.** The short state-of-the-art shows you know how others have studied similar phenomena. Not exhaustive; considered.
- **Study-design clarity.** Conditions chosen for a reason. Metrics motivated. Not "we tried some stuff."

**Point reductions:**

- All commits from one person, or commits from a shared account.
- Results that can't be reproduced from the committed repo.
- Prompts embedded as triple-quoted strings inside long functions instead of versioned files.
- Slides that restate the README instead of telling a story.
- "We all worked on everything" — no defensible individual contribution.
- Findings that are really feature lists (*"we implemented X, Y, Z"*) rather than observations about agent behavior.
- No logging, or `print()` scattered across notebooks passing as logs.

---

## 5. Final presentation — what to cover

**20 min for groups of up to 3 people, 30 min for groups of 4–5.** You don't have to follow this order rigidly, but everything below should be in there somewhere. Above all: **tell a story**, don't read a checklist at us.

Aim for a **number of slides below your number of minutes** — you can keep extra detail in **backup slides after the "The End" slide** and pull them up if a question calls for it, without cluttering the main talk.

- **Demo, if you have one.** Lead with it. A live or recorded demo earns more attention than any slide. Show a *base case* first so we understand the normal behavior, then the *interesting cases*. Don't manufacture interesting examples — but if you genuinely saw surprising, funny, or revealing ones, that's exactly what to show.
- **Problem focus.** Where did you actually put your energy? What do *you* see as the distinctive or interesting thing — the feature you built, or the question you studied? This is the heart of the talk.
- **Related work.** What areas did you look into? What did you learn and *reuse*? And — just as important — what did you *not* find, where you had to come up with an answer yourself?
- **What's agentic.** Which parts of your system are actually agentic, and which are plain code or a single model call? Which **different kinds of agents** do you have, and **what makes them different** — their job, their tools, their prompts, how much autonomy they have, how they hand off to each other? If it's a single agent, say so plainly.
- **What you expose, and how.** What **API or interface** does your system expose — via **MCP, an HTTP API, a tool interface, or other methods** — and why that choice? What can a client (or another agent) actually do through it?
- **Memory and context.** How do you manage **memory and context**? What gets remembered across turns and across sessions, where that state lives, and how you keep the context window relevant — retrieval, summarization, truncation, scratchpads. This is often where AI systems quietly succeed or fail.
- **Evaluation.** How did you design it? Which questions did you want to answer? Are there **quantitative metrics** — which and why? If **qualitative**, how did you assess it (rubric, raters, agreement)? Show concrete examples of where the system works well and — just as honestly — where it doesn't. Tie it back to the claim you set out to test.
- **What was hard.** The real obstacles — dead ends, things that didn't work, decisions you'd make differently.
- **Contribution of each team member.** Who did what, concretely. Every member should be able to speak to their own part.
