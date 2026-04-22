# Designing Large Scale AI Systems — Syllabus

> Designing Large Scale AI Systems is a CS Master course for students and practitioners who want to build AI-powered systems that actually work in production — not just demos. It teaches the engineering discipline of shipping reliable AI features into existing products, mastering the evaluation and improvement loop that keeps them reliable as they scale, and managing the complexity of systems where the runtime is probabilistic.

**Format:** 16 lessons across 4 phases, plus a capstone project. Spring 2026, 12 weeks.

**Convention:** each lesson has a page (HTML, serves as the in-class walkthrough) and — where applicable — a master Jupyter notebook alongside it in the same folder. Supporting `.py` scripts, exercises, solutions, and slides live in the same folder.

---

## Learning Objectives

By the end of this course, you will:

1. **Build Effective, Reliable AI Systems at Scale.** Solve complex problems by decomposing them in a principled way. Ship a reliable AI feature into an existing product.
2. **Use AI to Build AI.** Leverage AI for development, evaluation, and system management. Understand what this unlocks and where the limits are.
3. **Iterate Towards Success.** Master the science of monitoring, analysis, and estimation. Stand up an evaluation harness you can run in CI.
4. **Identify and Master the Key Abstractions.** Build observability, cost controls, and incident-ready guardrails. Take lessons from software engineering past, but do so critically.
5. **Think in Systems.** Understand which engineering principles carry forward from traditional software and which new abstractions are essential.

---

## Phase 1 — Building AI Agents

---

### L1 — Hello World

**Page:** `[labs/01_hello_world/hello_world_3.0.html](labs/01_hello_world/hello_world_3.0.html)`
**Tagline:** Connecting to AI via API: chat, streaming, voice, and image.

**Learning objectives**

- Understand the differences between non-AI software, ML-based software, and gen AI
- Know the different roles AI can play in software engineering
- Create a "hello world" AI-powered application
- Create a "hello world" application where AI is the *user*
- Create a "hello world" application *built using* AI

**Slides**

- *See lesson page and supporting materials in folder*

**Resources**

- Python scripts: `[1_chat.py](labs/01_hello_world/1_chat.py)`, `[2_streaming.py](labs/01_hello_world/2_streaming.py)`, `[3_voice.py](labs/01_hello_world/3_voice.py)`, `[4_image.py](labs/01_hello_world/4_image.py)`
- `[history-of-evals.md](labs/01_hello_world/history-of-evals.md)` / `[history-of-evals.html](labs/01_hello_world/history-of-evals.html)`

**Labs**

- Master notebook: `[lesson1_demo.ipynb](labs/01_hello_world/lesson1_demo.ipynb)`
- Homework: `[homework_01_ollama.ipynb](labs/01_hello_world/homework_01_ollama.ipynb)` — run a model locally with Ollama

---

### L2 — Mastering Individual AI Calls

**Page:** `[labs/02_standalone_agents/mastering_individual_calls.html](labs/02_standalone_agents/mastering_individual_calls.html)`
**Tagline:** Prompt engineering, structured outputs, best practices for reliable single calls.

**Learning objectives**

- Build an AI-powered application
- Master prompt engineering
- Separate what the *model* offers from the bells and whistles provided by individual API providers

**Slides**

- `[L2_v2_mastering_individual_calls.pdf](labs/02_standalone_agents/L2_v2_mastering_individual_calls.pdf)` — Mastering Individual Calls
- `[L2_Intro_with_and_for_ai.pdf](labs/02_standalone_agents/L2_Intro_with_and_for_ai.pdf)` — Roles of AI in Software

**Resources**

- `[L2_instructor_guide.md](labs/02_standalone_agents/L2_instructor_guide.md)`
- `[chat-completions-vs-responses-api.md](labs/02_standalone_agents/chat-completions-vs-responses-api.md)`
- `[prompts.md](labs/02_standalone_agents/prompts.md)`
- CLI scripts: `1_stateless_agent.py`, `2_stateful_agent.py`, `3_agent_with_memory.py`, `4_agent_with_long_term_memory.py` in `[labs/02_standalone_agents/](labs/02_standalone_agents/)`
- Prompt templates: `[prompting/](labs/02_standalone_agents/prompting/)`

**Labs**

- Master notebook: `[lesson2_demo.ipynb](labs/02_standalone_agents/lesson2_demo.ipynb)`
- Topic notebooks: `[lesson2_singlecall.ipynb](labs/02_standalone_agents/lesson2_singlecall.ipynb)`, `[lesson2_stateful.ipynb](labs/02_standalone_agents/lesson2_stateful.ipynb)`, `[lesson2_testing.ipynb](labs/02_standalone_agents/lesson2_testing.ipynb)`, `[lesson2_testing_and_metrics.ipynb](labs/02_standalone_agents/lesson2_testing_and_metrics.ipynb)`
- Exercises: `[lesson2_exercises.ipynb](labs/02_standalone_agents/lesson2_exercises.ipynb)`
- Answers: `[lesson2_answers.ipynb](labs/02_standalone_agents/lesson2_answers.ipynb)`
- Smoke tests: `[labs/tests/test_lesson_02_smoke.py](labs/tests/test_lesson_02_smoke.py)`

---

### L3 — Managing Context and Memory

**Page:** `[labs/03_context/stateless_stateful_agents.html](labs/03_context/stateless_stateful_agents.html)`
**Tagline:** Stateless & stateful agents, conversation history, cost & latency tradeoffs, memory strategies.

**Learning objectives**

- Understand the distinction between stateless and stateful interactions with AI
- Learn how to reason about the limit of *actual* vs. *effective* context for a given task
- Manage state across interactions
- Handle short- and long-term memory for effective stateful interactions

**Slides**

- `[L2_stateless_stateful_agents.pptx](labs/03_context/L2_stateless_stateful_agents.pptx)`

**Resources**

- CLI scripts: `1_stateless_agent.py`, `2_stateful_agent.py`, `3_agent_with_memory.py`, `4_agent_with_long_term_memory.py` in `[labs/03_context/](labs/03_context/)`
- `[prompt_templates/](labs/03_context/prompt_templates/)`

**Labs**

- Master notebook: `[lesson4_managing_context.ipynb](labs/03_context/lesson4_managing_context.ipynb)` (Python mirror: `lesson4_managing_context.py`)
- Exercises: `[lesson4_exercises.ipynb](labs/03_context/lesson4_exercises.ipynb)`
- Solutions: `[lesson4_solutions.ipynb](labs/03_context/lesson4_solutions.ipynb)`
- Review-loop tests: `[labs/tests/test_lesson_03_review_loop.py](labs/tests/test_lesson_03_review_loop.py)`

---

### L4 — Tools & Agentic Loops

**Page:** `[labs/04_tool_calling/tool_calling.html](labs/04_tool_calling/tool_calling.html)`
**Tagline:** Tool calling, function schemas, orchestration loops, when to call another tool vs. stop.

**Learning objectives**

- Design clear function schemas and tool descriptions that an LLM can reliably call
- Build an agentic loop: decide when to call a tool, when to call another, and when to stop
- Recognize the failure modes of agentic loops (infinite tools, silent failures, drift) and the control patterns that mitigate them

**Slides**

- `[tool_calling_slides.pptx](labs/04_tool_calling/tool_calling_slides.pptx)`

**Resources**

- Support modules: `[tools.py](labs/04_tool_calling/tools.py)`, `[tools_bad.py](labs/04_tool_calling/tools_bad.py)`, `[data_tools.py](labs/04_tool_calling/data_tools.py)`, `[data_tools_bad.py](labs/04_tool_calling/data_tools_bad.py)`
- `[prompt_templates/](labs/04_tool_calling/prompt_templates/)`

**Labs**

- Master notebook: `[lesson4b_tool_calling.ipynb](labs/04_tool_calling/lesson4b_tool_calling.ipynb)` (Python mirror: `lesson4b_tool_calling.py`)
- Exercises: `[lesson4b_exercises.ipynb](labs/04_tool_calling/lesson4b_exercises.ipynb)`
- Solutions: `[lesson4b_solutions.ipynb](labs/04_tool_calling/lesson4b_solutions.ipynb)`

---

## Phase 2 — "Eval" in Software 3.0: Iterating Towards Success

---

### L5 — "Eval" in Software 1.0 and 2.0

**Page:** `[labs/05_eval_fundamentals/datasets.html](labs/05_eval_fundamentals/datasets.html)`
**Tagline:** Foundations — evaluation in non-AI software and traditional ML, as the baseline every AI eval conversation builds on.

**Learning objectives**

- Understand why "eval" in AI systems is different from eval in non-AI software
- Review of eval in traditional software engineering
- Understand metrics and measurement for ML models
- Establish the vocabulary and datasets that Phase 2 will build on

**Slides**

- *TBD*

**Resources**

- `[datasets.md](labs/05_eval_fundamentals/datasets.md)`, `[outline.md](labs/05_eval_fundamentals/outline.md)`, `[auto_improvement_design.md](labs/05_eval_fundamentals/auto_improvement_design.md)`
- `[best_practices.yaml](labs/05_eval_fundamentals/best_practices.yaml)`
- Pipeline scripts: `[pipeline.py](labs/05_eval_fundamentals/pipeline.py)`, `run_eval_ground_truth.py`, `run_extract.py`, `run_judge.py`, `run_improve.py`, `run_loop.py`, `autotune.py`
- Prompt templates: `[prompt_templates/](labs/05_eval_fundamentals/prompt_templates/)`

**Labs**

- `[browse_datasets.ipynb](labs/05_eval_fundamentals/browse_datasets.ipynb)` — explore the eval datasets
- `[iteration_loop.ipynb](labs/05_eval_fundamentals/iteration_loop.ipynb)` — run the end-to-end improvement loop

---

### L6 — Iterating in the Dark: Organizational Blindness in AI Evaluations

**Page:** `[labs/06_mastering_uncertainty/optimizing-in-the-dark/index.html](labs/06_mastering_uncertainty/optimizing-in-the-dark/index.html)`
**Tagline:** Structural flaws, uncertainty vs. variability confusion, and the cost of ignorance — how well-intentioned eval pipelines go wrong.

**Learning objectives**

- Recognize the most common structural flaws in AI evals (leakage, selection bias, confounding with prompt changes, scorecard gaming)
- Distinguish *uncertainty* from *variability* — and know which tools address each
- Diagnose eval failures in your own pipelines and design processes that make blind spots visible before they ship

**Slides**

- *TBD*

**Resources**

- Parts: `[part-1-structural-flaw.md](labs/06_mastering_uncertainty/optimizing-in-the-dark/part-1-structural-flaw.md)`, `[part-2-cost-of-ignorance.md](labs/06_mastering_uncertainty/optimizing-in-the-dark/part-2-cost-of-ignorance.md)`, `[part-2b-uncertainty-vs-variability.md](labs/06_mastering_uncertainty/optimizing-in-the-dark/part-2b-uncertainty-vs-variability.md)`
- `[glossary.md](labs/06_mastering_uncertainty/optimizing-in-the-dark/glossary.md)`
- `[Optimizing in the Dark.docx](labs/06_mastering_uncertainty/Optimizing%20in%20the%20Dark.docx)`

**Labs**

- *No notebook yet — content is narrative HTML/markdown.*

---

### L7 — "Eval" in Software 3.0 (AI Agents)

**Page:** `[labs/07_eval/eval_sw3.html](labs/07_eval/eval_sw3.html)`
**Tagline:** From traditional eval to evaluating AI agents — datasets, judges, and the iteration loop for unstructured output.

**Learning objectives**

- Learn basic methods for evaluating unstructured output
- Understand the anatomy of an AI eval pipeline: extract → judge → improve → loop
- Stand up an evaluation harness you can run repeatedly and in CI

**Slides**

- *TBD*

**Resources**

- `[outline.md](labs/07_eval/outline.md)`, `[auto_improvement_design.md](labs/07_eval/auto_improvement_design.md)`
- `[best_practices.yaml](labs/07_eval/best_practices.yaml)`
- Pipeline scripts: `[pipeline.py](labs/07_eval/pipeline.py)`, `run_eval_ground_truth.py`, `run_extract.py`, `run_judge.py`, `run_improve.py`, `run_loop.py`, `autotune.py`, `download_datasets.py`
- Prompt templates: `[prompt_templates/](labs/07_eval/prompt_templates/)`

**Labs**

- `[browse_datasets.ipynb](labs/07_eval/browse_datasets.ipynb)`
- `[iteration_loop.ipynb](labs/07_eval/iteration_loop.ipynb)`
- Eval lab session: `[labs/11_lab_eval_session/](labs/11_lab_eval_session/)` — hands-on exercise with articles, guidelines, and `[notebook.ipynb](labs/11_lab_eval_session/notebook.ipynb)`

---

### L8 — Designing Experiments and Mastering Uncertainty — Part I

**Page:** `[labs/08_automating_improvement/design_of_experiments.html](labs/08_automating_improvement/design_of_experiments.html)`
**Tagline:** Apply the uncertainty toolkit to real AI systems — design experiments, quantify what you don't know, report it honestly.

**Learning objectives**

- Frame an AI eval as an *estimator* of a random variable (the system's true behaviour on a population of inputs) — not a point measurement
- Design experiments that separate signal from noise
- Choose metrics and reporting formats that expose variance rather than hide it

**Slides**

- `[labs/08_automating_improvement/slides_p/](labs/08_automating_improvement/slides_p/)`

**Resources**

- `[uncertainty_sources_design.md](labs/08_automating_improvement/uncertainty_sources_design.md)`
- Interactive playgrounds: `[AI Evaluation Playgrounds](playground/index.html)` — each play lets you *feel* a source of uncertainty and see how to *fix* it
- Statistics foundations: `[N Coin Flips / CLT](playground/Convolution%20of%20Independent%20Random%20Variables.html)`, `[Bootstrap Lab](playground/bootstrap_lab.html)`, `[Distribution Explorer](playground/distribution_explorer.html)`

**Labs**

- Overfitting lab: `[overfitting_lab.ipynb](labs/08_automating_improvement/overfitting_lab.ipynb)` (Python mirror: `overfitting_lab.py`)

---

### L9 — Designing Experiments and Mastering Uncertainty — Part II

**Page:** `[labs/08_automating_improvement/design_of_experiments_2.html](labs/08_automating_improvement/design_of_experiments_2.html)`
**Tagline:** Deeper into uncertainty and brittleness — bootstrapping, Beta posteriors, and the sources of uncertainty that actually matter in practice.

**Learning objectives**

- Quantify uncertainty in estimates (confidence intervals, bootstrapping, Beta posteriors)
- Decide which uncertainty is worth reducing vs. accepting
- Understand the sources of uncertainty and measure their impact: a real concern or a remote theoretical risk?
- Recognize organizational patterns that produce blind spots (incentive misalignment, reporting, metric ownership)

**Slides**

- `[labs/08_automating_improvement/slides_p/](labs/08_automating_improvement/slides_p/)`

**Resources**

- Sources of uncertainty (pick through these in class): `[Sampling Noise](playground/sampling_noise.html)`, `[Sampling Bias](playground/sampling_bias.html)`, `[Multiple Hypothesis Testing](playground/multiple_hypothesis_testing.html)`, `[Variance Across Domains](playground/domain_variance.html)`, `[Choice of Metric](playground/metric_choice.html)`, `[Temporal Drift](playground/temporal_drift.html)`, `[LLM Evolution](playground/llm_evolution.html)`, `[Judges & Compounding](playground/judges_and_compounding.html)`
- `[Accuracy Estimator](playground/accuracy_estimator.html)` — Beta-posterior point estimate + credible interval for a pass-rate

**Labs**

- Prompt-brittleness lab: `[prompt_brittleness_lab.ipynb](labs/08_automating_improvement/prompt_brittleness_lab.ipynb)` (Python mirror: `prompt_brittleness_lab.py`)

---

### L10 — Monitoring, Observability, and Reporting

**Page:** `[labs/09_monitoring/monitoring.html](labs/09_monitoring/monitoring.html)`
**Tagline:** What to monitor, how to monitor it, and how to turn traces into statistical assertions you can trust.

**Learning objectives**

- Learn what and how to monitor
- Diagnose individual calls, monitor sessions, monitor whole systems
- Understand traces and statistical assertions

**Slides**

- `[monitoring_slides.html](labs/09_monitoring/monitoring_slides.html)`
- `[monitoring_slides.pptx](labs/09_monitoring/monitoring_slides.pptx)`

**Resources**

- `[README.md](labs/09_monitoring/README.md)`, `[outline.md](labs/09_monitoring/outline.md)`, `[slides_outline.md](labs/09_monitoring/slides_outline.md)`
- `[demos/](labs/09_monitoring/demos/)`, `[exercises/](labs/09_monitoring/exercises/)`, `[solutions/](labs/09_monitoring/solutions/)`
- `[minimal_agent.py](labs/09_monitoring/minimal_agent.py)`, `[trace_viewer.py](labs/09_monitoring/trace_viewer.py)`, `[weekly_report_demo.py](labs/09_monitoring/weekly_report_demo.py)`
- `[golden_set.json](labs/09_monitoring/golden_set.json)`

**Labs**

- Master notebook: `[monitoring_lab.ipynb](labs/09_monitoring/monitoring_lab.ipynb)` (Python mirror: `monitoring_lab.py`)

---

## Phase 3 — Building and Managing Complex Systems

---

### L11 — Complex Systems I: Councils and Agentic Patterns

**Page:** `[labs/10_complex_systems/1_councils/councils.html](labs/10_complex_systems/1_councils/councils.html)`
**Tagline:** Council of Agents and other agentic patterns — self-consistency, role-based panels, multi-model ensembles, diverse-judge.

**Learning objectives**

- Recognize the main council/ensemble patterns and what each buys you
- Understand when disagreement is a *feature* (calibrated uncertainty from independent errors) vs. a *failure mode* (correlated errors)
- Reason about the core design questions of multi-agent systems: diversity, aggregation, cost, and evaluation

**Slides**

- `[agentic_patterns.slides.md](labs/10_complex_systems/1_councils/agentic_patterns.slides.md)`

**Resources**

- `[councils_concept.md](labs/10_complex_systems/1_councils/councils_concept.md)`

**Labs**

- *No notebook yet.*

---

### L12 — Complex Systems II: Foundational Programming Abstractions

**Pages:**

- `[labs/10_complex_systems/2_abstractions/key_abstractions.html](labs/10_complex_systems/2_abstractions/key_abstractions.html)` — key abstractions
- `[labs/06_ai-api/aoa.html](labs/06_ai-api/aoa.html)` — Abstractions of Agents
- `[labs/06_ai-api/ai_tools_integration.html](labs/06_ai-api/ai_tools_integration.html)` — AI tools integration
- `[labs/06_ai-api/mcp_tutorial.html](labs/06_ai-api/mcp_tutorial.html)` — MCP tutorial

**Tagline:** Foundational programming abstractions for AI systems — agentic loops, autonomy sliders, context/memory, tool integration surfaces, and MCP.

**Learning objectives**

- Identify the foundational abstractions for AI systems — agentic loops, autonomy sliders, context/memory, tool-integration surfaces — and know when to reach for each
- Understand what MCP is, what problem it solves, and how agent-system integration is standardizing
- Map a concrete AI feature to the right abstractions, so code stays manageable as the system grows

**Slides**

- `[aoa.pdf](labs/06_ai-api/aoa.pdf)` / `[aoa.pptx](labs/06_ai-api/aoa.pptx)` / `[aoa-improved.pptx](labs/06_ai-api/aoa-improved.pptx)` — Abstractions of Agents

**Resources**

- Abstractions & interfaces: `[ai_interface.md](labs/06_ai-api/ai_interface.md)`, `[agentic_loop.md](labs/06_ai-api/agentic_loop.md)`, `[autonomy_slider.md](labs/06_ai-api/autonomy_slider.md)`, `[context_memory.md](labs/06_ai-api/context_memory.md)`, `[designing_agentic_systems.md](labs/06_ai-api/designing_agentic_systems.md)`
- Tool calling / MCP: `[ai_tools_integration.md](labs/06_ai-api/ai_tools_integration.md)`, `[mcp_tutorial.md](labs/06_ai-api/mcp_tutorial.md)`, `[mcp_tool_calling_and_ai_integration_surfaces.md](labs/06_ai-api/mcp_tool_calling_and_ai_integration_surfaces.md)`, `[mcp-logging-observability.md](labs/06_ai-api/mcp-logging-observability.md)`
- AoA variant: `[aoa2.md](labs/06_ai-api/aoa2.md)` / `[aoa2.html](labs/06_ai-api/aoa2.html)`
- Safety & testing: `[safety_guardrails.md](labs/06_ai-api/safety_guardrails.md)`, `[testing_observability.md](labs/06_ai-api/testing_observability.md)`
- `[LECTURE_REVIEW_2026.md](labs/06_ai-api/LECTURE_REVIEW_2026.md)`

**Labs**

- *No notebook yet.*

---

### L13 — Complex Systems III: Reliable System Architectures

**Page:** `[labs/10_complex_systems/3_architectures/complex_systems.html](labs/10_complex_systems/3_architectures/complex_systems.html)`
**Tagline:** Architecture patterns that keep AI systems reliable under real traffic — timeouts, fallbacks, budgets, graceful degradation.

**Learning objectives**

- Apply architecture patterns that keep AI systems reliable under production traffic
- Design for graceful degradation, blast-radius control, and incident-readiness
- Plan for multi-version considerations — prompts, tools, schemas, datasets — so upgrades don't silently regress behaviour

**Slides**

- *TBD*

**Resources**

- *TBD*

**Labs**

- *No notebook yet.*

---

### L14 — Structuring Complex Projects

**Page:** `[labs/12_structuring_projects/structuring_projects.html](labs/12_structuring_projects/structuring_projects.html)`
**Tagline:** Shipping into existing products, maintaining large AI systems, multi-version considerations.

**Learning objectives**

- Structure projects for shipping into existing products and maintaining them across model and prompt versions
- Organize code, prompts, datasets, and evals so the system stays legible as it grows
- Plan for version upgrades (model, prompt, schema) without silent behaviour regressions

**Slides**

- *TBD*

**Resources**

- *TBD*

**Labs**

- *No notebook yet.*

---

### L15 — Programming in English (Without Losing Control)

**Page:** `[labs/13_programming_in_english/programming_in_english.html](labs/13_programming_in_english/programming_in_english.html)`
**Tagline:** Using AI to build software, without ceding the engineering judgment that keeps systems sane.

**Learning objectives**

- Use AI to accelerate software development (code generation, review, refactoring) without losing the engineering judgment that keeps systems sane
- Understand why natural language is a lossy specification medium — and what that means for correctness, control, and debuggability
- Establish a sustainable working style for AI-assisted development: when to trust, when to verify, when to step in

**Slides**

- *TBD*

**Resources**

- *TBD*

**Labs**

- *No notebook yet.*

---

### L16 — Using AI Frameworks

**Page:** `[labs/14_frameworks/frameworks.html](labs/14_frameworks/frameworks.html)`
**Tagline:** When and why to use frameworks; LangChain, LangGraph, LlamaIndex as case studies.

**Learning objectives**

- Explain what frameworks actually provide beyond "less code" — integrations, standard patterns, observability hooks, and ecosystem — and what they don't
- Compare LangChain, LlamaIndex, and LangGraph along three axes (orchestration, data/retrieval, state) and pick an appropriate tool for a given problem
- Apply a decision rule for when a framework is a net positive vs. a net negative — and what the "framework tax" looks like for your system

**Slides**

- *TBD*

**Resources**

- `[outline.md](labs/14_frameworks/outline.md)`
- Agent implementations: `[agent_scratch.py](labs/14_frameworks/agent_scratch.py)`, `[agent_langchain.py](labs/14_frameworks/agent_langchain.py)`, `[agent_langgraph.py](labs/14_frameworks/agent_langgraph.py)`, `[agent_llamaindex.py](labs/14_frameworks/agent_llamaindex.py)`
- Shared tools: `[tools_shared.py](labs/14_frameworks/tools_shared.py)`

**Labs**

- Master notebook: `[agent_comparison.ipynb](labs/14_frameworks/agent_comparison.ipynb)`

---

## Phase 4 — Capstone Project

The capstone project runs for roughly six weeks and is where the course's ideas meet a real system. Students pick a track (team, up to 5 students, or individual), ship an AI feature end-to-end, and present.

---

### L17–L18 — Project Specification & Midterm

**Tagline:** Track selection, requirements, project kick-off — plus the individual written exam covering Lessons 1–16.

**Project outline**

- `[projects.html](projects.html)` — project tracks, rubric, deliverables
- `[assessments.html](assessments.html)` — midterm exam scope and policy
- `[mock_exams/ai_mock_midterm_w_sol.html](mock_exams/ai_mock_midterm_w_sol.html)` — mock midterm (with solutions)
- `[mock_exams/additional_questions_w_sol.html](mock_exams/additional_questions_w_sol.html)` — additional practice

---

### L19–L22 — Project Working Sessions

**Tagline:** Problem statement, architecture diagram, evaluation plan — implementation, first evaluation run, peer reviews.

**Deliverables across sprints**

- Problem statement + architecture diagram
- Evaluation plan (datasets, metrics, judges, confidence reporting)
- Implementation + first evaluation run
- Peer review and iteration

---

### L23–L24 — Final Presentations & Retrospective

**Tagline:** Graded presentations with Q&A, project review, course wrap-up.

---

## Assessment

| Component | Weight | Format |
| --- | --- | --- |
| Part I: Midterm Exam (Individual) | 30% | Written, closed book, 60 minutes |
| Part II: Course Project | 70% | In-class, assisted, attendance required (Track A) or individual, unassisted (Track B); four sprints plus presentation |

Midterm scope and policies: `[assessments.html](assessments.html)`. Project tracks, rubric, and documents: `[projects.html](projects.html)`.

---

## Setup & Environment

- Clone the repo, install `uv`, configure API keys, install Ollama for the L1 homework
- Python entry point: `[main.py](main.py)` · dependency manifest: `[pyproject.toml](pyproject.toml)`
- Course homepage: `[index.html](index.html)` · contact: `[about.html](about.html)`

---

## Interactive Playgrounds

The `[playground/](playground/index.html)` directory is a library of small, runnable demos that let students *feel* a statistical or behavioural property of AI systems rather than just read about it. Used throughout Phase 2:

- Statistics foundations: `[N Coin Flips / CLT](playground/Convolution%20of%20Independent%20Random%20Variables.html)`, `[Bootstrap Lab](playground/bootstrap_lab.html)`, `[Distribution Explorer](playground/distribution_explorer.html)`, `[Accuracy Estimator](playground/accuracy_estimator.html)`
- Sources of uncertainty: `[Sampling Noise](playground/sampling_noise.html)`, `[Sampling Bias](playground/sampling_bias.html)`, `[Multiple Hypothesis Testing](playground/multiple_hypothesis_testing.html)`, `[Variance Across Domains](playground/domain_variance.html)`, `[Choice of Metric](playground/metric_choice.html)`, `[Temporal Drift](playground/temporal_drift.html)`, `[LLM Evolution](playground/llm_evolution.html)`, `[Judges & Compounding](playground/judges_and_compounding.html)`

---

## Orphan content (not yet mapped)

- `[labs/representations/](labs/representations/)` — `slides.md`. Unclear mapping.
- `[labs/06_ai-api/gpt_propsal_for_abstractions.html](labs/06_ai-api/gpt_propsal_for_abstractions.html)` — draft proposal; reference material for L12.
