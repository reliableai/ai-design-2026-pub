# Tool Calling Assignment: Build a Conversational Agent with Tools

## What you'll build

A conversational AI assistant that uses the OpenAI Chat Completion API with **tool calling**. Your assistant talks to a user in natural language and uses three tools behind the scenes to take actions and answer questions.

You'll use Claude, Copilot, or any AI assistant to help you code — but you need to **understand what's happening**. At the end, you should be able to explain the full message flow for any conversation turn.

## Pick a theme

Choose **one** of three themes. They all work the same way — same mechanics, different flavor.

| Theme | Folder | Setting |
|-------|--------|---------|
| **Dungeon Master's Helper** | `dungeon_master/` | A tabletop RPG assistant that helps resolve player actions |
| **Hogwarts Wizard Assistant** | `harry_potter/` | A magical assistant for spells, potions, and creatures |
| **Space Mission Planner** | `space_mission/` | A mission control assistant for interplanetary travel |

Each folder contains:
- `data.py` — the hardcoded data, system prompt, and starter conversations (don't modify this)
- `starter.py` — a skeleton to get you going (you can use this, start from scratch, use a notebook — whatever you prefer)

Work inside your chosen folder. Import the data with `from data import *`.

## What you need to implement

### 1. Tool functions

Three simple Python functions that look up data and return a dict. These are already stubbed out in `solution.py` — just fill them in. They're intentionally trivial (dictionary lookups, basic math) so you can focus on the wiring.

### 2. Tool schemas

The JSON descriptions that tell the model what tools are available, what parameters they take, and what they do. You write these. Getting them right matters — a vague schema leads to bad tool calls.

### 3. The conversation loop

This is the core of the assignment. Your loop must:

1. Send the conversation history + tool schemas to `client.chat.completions.create()`
2. Check the response: did the model return `tool_calls` or a regular message?
3. If `tool_calls`: execute each one, append the results as `tool` role messages, and **call the API again** (the model may need to call more tools or synthesize the results)
4. If regular message: print it — you're done for this turn
5. Repeat until the model responds to the user (or you hit a safety limit)

### 4. Conversation memory

The model has no memory of its own — it only knows what you send in the message list. You need to implement **two approaches** and compare them:

**Approach A: Full history (the naive way).** Send the entire conversation every time. This is the simplest thing that works — start here to get everything running. But notice what happens: the message list grows with every turn, and it includes all the tool call/result pairs (which are verbose). After 10+ turns, you're sending a lot of tokens.

**Approach B: Managed memory.** Instead of sending everything, you actively manage what the model sees. The idea: use the LLM itself to summarize older parts of the conversation, then send only the summary + the most recent turns. Concretely:

1. After every N turns (say, 4-6), ask the LLM to summarize the conversation so far in a few sentences
2. Replace the old messages with that summary (as a system message)
3. Keep only the last few turns in full detail
4. Continue the conversation with this compressed context

This is a real technique used in production systems. The trade-off: you save tokens and money, but the summary might lose details the user later refers to. Your job is to implement it, see where it breaks, and understand why.

**Test both approaches** with a conversation of 8+ turns where the user refers back to something from the beginning. Does the managed version still work? What does it lose?

### 5. Logging

Print the full message list at each iteration of the loop. For every API call, show:
- What messages you're sending
- Whether the model responded with tool calls or text
- If tool calls: which tools, what arguments, what results

This isn't just for debugging — it's how you prove you understand what's happening.

## Starter conversations

Each theme file includes 4 test scenarios, designed to exercise specific concepts:

| # | Tests | What should happen |
|---|-------|--------------------|
| 1 | **No tools needed** | Model answers from context/system prompt alone |
| 2 | **Single tool call** | Model calls one tool, gets result, responds |
| 3 | **Multi-tool chain** | Model calls 2+ tools in sequence before responding |
| 4 | **Memory across turns** | Model must remember something from earlier in the conversation |
| 5 | **Memory management** | A longer conversation (8+ turns) where you test both full-history and managed-memory approaches |

Run all five. If they work, you understand the basics.

Then try your own conversations — break things, see what happens when the model hallucinates a tool that doesn't exist, when it passes wrong arguments, when the conversation gets long.

## Evaluate your assistant

Once your system works, build a simple **LLM-as-judge** evaluation. The idea: run your starter conversations automatically, then ask a separate LLM call to judge whether the assistant behaved correctly.

### What to do

1. **Create a Jinja2 template** (`judge.j2`) for the judge prompt. The template receives the full conversation (user messages, tool calls, tool results, assistant responses) and evaluates it against criteria like:
   - Did the assistant use tools when it should have? (e.g., it shouldn't answer a spell question from memory)
   - Did it avoid calling tools when it didn't need to? (e.g., a greeting doesn't need a tool)
   - Were the tool arguments correct?
   - Was the final answer consistent with the tool results?
   - For multi-turn: did memory work — did the assistant remember earlier context?

2. **Run each starter conversation** through your system programmatically (not interactively), capturing the full message history.

3. **Pass each conversation to the judge** using your Jinja2 template. The judge should return a structured response — at minimum a pass/fail and a short explanation for each criterion.

4. **Print a summary** — which tests passed, which failed, and why.

### Why this matters

You're learning to evaluate AI systems, not just build them. A working system that you can't evaluate is a system you can't improve. The judge prompt is itself a prompt engineering exercise — how do you describe "correct behavior" precisely enough for an LLM to assess it?

## Deliverable

A working system — Jupyter notebook, Python script, or a simple UI (Streamlit, Gradio, whatever you like). Someone should be able to run it and have a conversation with your assistant. Include your `judge.j2` template and the evaluation results for the starter conversations.

## Example

The `harry_potter/` folder contains `example.py` and `example.ipynb` — a complete working implementation. It shows one way to do everything: tool functions, schemas, the conversation loop with full history, managed memory with LLM-driven summarization, and a side-by-side comparison of both approaches. Read it after you've tried yourself — or peek at it if you're stuck.

## Setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
uv sync
```

Or if you prefer pip:
```bash
pip install openai python-dotenv
```

Copy `.env.example` to `.env` and add your key:
```bash
cp .env.example .env
# then edit .env with your key
```

**Do NOT commit your `.env` file or your API key to git.** Add `.env` to your `.gitignore` or just be careful. If you accidentally push a key, revoke it immediately in the OpenAI dashboard.

## VS Code tip

If you use VS Code and want output text to wrap in your notebook: go to **Settings** → search for `notebook output word wrap` → enable it.

## Tips

- **Start small.** Get a single tool call working before you try chaining.
- **Print everything.** When something goes wrong, the message list tells you exactly where.
- **Read the API response carefully.** `message.tool_calls` is a list — even for a single call.
- **`tool_call_id` matters.** Each tool result must reference the specific `tool_call_id` it's responding to.
- **The system prompt shapes behavior.** A good system prompt tells the model when to use tools vs. when to just talk.
- **Don't trust the model blindly.** It might call a tool with wrong arguments, or call tools when it shouldn't. That's part of the learning.
