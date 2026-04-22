# %% [markdown]
# # Hogwarts Wizard Assistant — Example Implementation
#
# A working example for the tool-calling assignment.
# Shows one way to implement the tools, schemas, conversation loop, and memory.
#
# **This is a reference implementation — not the only way to do it.**

# %%
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()
MODEL = "gpt-5"
print(f"Client ready — using {MODEL}")

# %% [markdown]
# ## 1. Data
#
# Imported from the theme file. Nothing to implement here.

# %%
from data import (
    SPELLS, POTIONS, ALL_INGREDIENTS, CREATURES,
    SYSTEM_PROMPT, STARTER_CONVERSATIONS,
)

print(f"Loaded: {len(SPELLS)} spells, {len(POTIONS)} potions, {len(CREATURES)} creatures")

# %% [markdown]
# ## 2. Tool Functions
#
# Three simple lookups. The key thing: they return dicts (which we'll
# serialize to JSON for the API), and they handle missing data with
# an `"error"` field instead of raising exceptions.

# %%
def cast_spell(spell_name: str) -> dict:
    """Look up a spell by name."""
    key = spell_name.strip().lower()
    if key in SPELLS:
        return {"spell": key, **SPELLS[key]}
    return {"error": f"Spell '{spell_name}' not found. Known spells: {', '.join(SPELLS.keys())}"}


def brew_potion(ingredients: list) -> dict:
    """Check if a set of ingredients makes a known potion."""
    normalized = frozenset(i.strip().lower() for i in ingredients)
    if normalized in POTIONS:
        return {"ingredients": sorted(normalized), **POTIONS[normalized]}
    return {
        "error": "No known potion with these ingredients.",
        "you_provided": sorted(normalized),
        "known_ingredients": ALL_INGREDIENTS,
    }


def lookup_creature(name: str) -> dict:
    """Look up a magical creature by name."""
    key = name.strip().lower()
    if key in CREATURES:
        return {"creature": key, **CREATURES[key]}
    return {"error": f"Creature '{name}' not found. Known creatures: {', '.join(CREATURES.keys())}"}


# Quick sanity check — these are all invented, the LLM can't know them
print(json.dumps(cast_spell("Vortexia"), indent=2))
print(json.dumps(brew_potion(["moonpetal", "crystallized fog"]), indent=2))
print(json.dumps(lookup_creature("gloomfang"), indent=2))

# %% [markdown]
# ## 3. Tool Schemas
#
# These JSON descriptions tell the model what tools exist.
# The quality of names, descriptions, and parameter types
# directly affects how well the model picks the right tool.

# %%
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "cast_spell",
            "description": (
                "Look up a spell by name. Returns the spell's type (offensive/defensive/utility), "
                "effect, difficulty level, and power rating. Use this when the user asks about a "
                "specific spell or when you need to find a spell to counter a creature."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "spell_name": {
                        "type": "string",
                        "description": "The name of the spell, e.g. 'vortexia', 'glacius torrent'",
                    },
                },
                "required": ["spell_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "brew_potion",
            "description": (
                "Check if a combination of ingredients produces a known potion. "
                "Pass the full list of ingredients. Returns the potion name, effect, "
                "difficulty, and brewing time if the combination is valid. "
                "If invalid, returns an error with the list of all known ingredients."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ingredients": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of ingredient names, e.g. ['moonpetal', 'crystallized fog']",
                    },
                },
                "required": ["ingredients"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_creature",
            "description": (
                "Look up a magical creature by name. Returns its danger level (X to XXXXX), "
                "description, weaknesses, abilities, and habitat. "
                "Use this before suggesting how to deal with a creature."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The creature's name, e.g. 'gloomfang', 'mistwalker'",
                    },
                },
                "required": ["name"],
            },
        },
    },
]

TOOLS = {
    "cast_spell": cast_spell,
    "brew_potion": brew_potion,
    "lookup_creature": lookup_creature,
}

print(f"Registered {len(TOOL_SCHEMAS)} tool schemas:")
for s in TOOL_SCHEMAS:
    print(f"  - {s['function']['name']}")

# %% [markdown]
# ## 4. The Conversation Loop
#
# This is the core. The loop:
# 1. Sends messages + schemas to the API
# 2. If the model returns `tool_calls` → execute each, append results, call again
# 3. If the model returns text → we're done for this turn
#
# **Note on logging:** we print the full flow at each step. This isn't optional —
# it's how you understand what's actually happening between your code and the API.

# %%
def tool_loop(messages, max_iterations=10):
    """Run the tool-calling loop until the model produces a text answer.

    Args:
        messages: the full message list (modified in place)
        max_iterations: safety limit to prevent infinite loops

    Returns:
        The model's final text response
    """
    for i in range(1, max_iterations + 1):
        print(f"\n--- Iteration {i} ---")
        print(f"Sending {len(messages)} messages to API...")

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
        )

        msg = response.choices[0].message

        # Case 1: model wants to call tools
        if msg.tool_calls:
            print(f"Model requests {len(msg.tool_calls)} tool call(s):")
            messages.append(msg)  # append the assistant message with tool_calls

            for tc in msg.tool_calls:
                fn_name = tc.function.name
                fn_args = json.loads(tc.function.arguments)
                print(f"  → {fn_name}({json.dumps(fn_args)})")

                # execute the tool
                if fn_name in TOOLS:
                    result = TOOLS[fn_name](**fn_args)
                else:
                    result = {"error": f"Unknown tool: {fn_name}"}

                result_json = json.dumps(result)
                print(f"    Result: {result_json[:150]}{'...' if len(result_json) > 150 else ''}")

                # append the tool result — must reference the specific tool_call_id
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result_json,
                })

        # Case 2: model responds with text — we're done
        else:
            print(f"Model responds with text.")
            messages.append(msg)
            return msg.content

    return "[Max iterations reached — the model kept calling tools without answering]"


print("tool_loop() ready.")

# %% [markdown]
# ## 5. Run the Starter Conversations
#
# Each one tests a different concept. Watch the logs to see what happens.

# %% [markdown]
# ### Test 1: No tools needed
# The model should just answer from the system prompt — no tool calls.

# %%
test1 = STARTER_CONVERSATIONS[0]
print(f"=== {test1['test']} ===")
print(f"User: {test1['message']}\n")

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": test1["message"]},
]
answer = tool_loop(messages)
print(f"\nAssistant: {answer}")

# %% [markdown]
# ### Test 2: Single tool call
# The model should call `cast_spell` once, then answer.

# %%
test2 = STARTER_CONVERSATIONS[1]
print(f"=== {test2['test']} ===")
print(f"User: {test2['message']}\n")

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": test2["message"]},
]
answer = tool_loop(messages)
print(f"\nAssistant: {answer}")

# %% [markdown]
# ### Test 3: Multi-tool chain
# The model should call `lookup_creature("mistwalker")`, see that the weakness
# is the Clamorous spell, then call `cast_spell("clamorous")` to learn about it.
# Two tool calls, possibly in sequence (two iterations) or parallel (one iteration).

# %%
test3 = STARTER_CONVERSATIONS[2]
print(f"=== {test3['test']} ===")
print(f"User: {test3['message']}\n")

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": test3["message"]},
]
answer = tool_loop(messages)
print(f"\nAssistant: {answer}")

# %% [markdown]
# ### Test 4: Memory across turns
# Two messages in the same conversation. The second one only makes sense
# if the model remembers what happened in the first turn.

# %%
test4 = STARTER_CONVERSATIONS[3]
print(f"=== {test4['test']} ===")

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

for i, user_msg in enumerate(test4["messages"]):
    print(f"\n{'='*50}")
    print(f"Turn {i+1}")
    print(f"User: {user_msg}")
    messages.append({"role": "user", "content": user_msg})
    answer = tool_loop(messages)
    print(f"\nAssistant: {answer}")

# %% [markdown]
# ## 6. Memory Management
#
# So far, we've been sending the **entire** message list every time. That works,
# but look at what's in that list after just 3-4 turns: system prompt, user messages,
# assistant messages with tool_calls objects, tool result messages (often verbose JSON)...
# it adds up fast.
#
# The idea: use the LLM itself to **summarize** older parts of the conversation,
# then send only the summary + the most recent turns in full.

# %%
def _get(m, key, default=""):
    """Get a field from a message dict or pydantic object."""
    if isinstance(m, dict):
        return m.get(key, default)
    return getattr(m, key, default)


def count_messages(messages):
    """Count messages and estimate rough token usage."""
    total_chars = sum(len(str(_get(m, "content", ""))) for m in messages)
    return len(messages), total_chars


def summarize_conversation(messages):
    """Ask the LLM to summarize the conversation so far.

    This is itself an API call — so summarization has a cost too.
    But the summary is much shorter than the full history.
    """
    # Extract only the human-readable parts (skip raw tool call objects)
    readable = []
    for m in messages:
        role = _get(m, "role", "")
        content = _get(m, "content", "")
        if role == "user":
            readable.append(f"User: {content}")
        elif role == "assistant" and isinstance(content, str) and content:
            readable.append(f"Assistant: {content}")
        elif role == "tool":
            readable.append(f"Tool result: {str(content)[:100]}...")

    summary_request = [
        {"role": "system", "content": (
            "Summarize this conversation in 3-4 sentences. "
            "Focus on: what the user asked about, what key facts were established "
            "(spell names, creature weaknesses, potion recipes), and any ongoing plans. "
            "Be specific — include names and details the user might refer back to."
        )},
        {"role": "user", "content": "\n".join(readable)},
    ]
    response = client.chat.completions.create(model=MODEL, messages=summary_request)
    return response.choices[0].message.content


def compress_messages(messages, keep_recent=4):
    """Compress older messages into a summary, keep recent ones in full.

    Args:
        messages: the full message list
        keep_recent: how many recent user turns to keep in full

    Returns:
        A new (shorter) message list with a summary replacing older messages.
    """
    # Find the indices where user messages start (each "turn")
    user_indices = [i for i, m in enumerate(messages) if _get(m, "role") == "user"]

    # If we don't have enough turns to compress, return as-is
    if len(user_indices) <= keep_recent:
        return messages

    # Split: everything before the Nth-to-last user message gets summarized
    cut_point = user_indices[-keep_recent]
    old_messages = messages[1:cut_point]  # skip system prompt
    recent_messages = messages[cut_point:]

    summary = summarize_conversation(old_messages)

    return [
        messages[0],  # original system prompt
        {"role": "system", "content": f"Summary of earlier conversation:\n{summary}"},
        *recent_messages,
    ]


print("Memory management functions ready.")

# %% [markdown]
# ### Test 5: A long conversation — full history vs. managed memory
#
# We'll run the same 8-turn conversation twice:
# once with full history (Approach A), once with managed memory (Approach B).
# The last message refers back to turn 1 — does the managed version still get it?

# %%
# A scripted 8-turn conversation that builds up context and then tests recall.
LONG_CONVERSATION = [
    "What does the Vortexia spell do?",
    "Interesting. What about Glacius Torrent?",
    "I found some moonpetal and crystallized fog. What can I brew?",
    "Now tell me about the Gloomfang creature.",
    "What spell would work against a Sporemother?",
    "I also have lavender honey and ghost orchid — what potion is that?",
    "Let's go back to the beginning — which of the two spells I asked about first would be better for defending against a Thornback?",
    "And remind me — what was the potion I could brew with moonpetal?",
]

# %% [markdown]
# #### Approach A: Full history
# Send everything, every time. Simple and correct, but watch the message count grow.

# %%
print("=" * 60)
print("APPROACH A: Full History")
print("=" * 60)

messages_full = [{"role": "system", "content": SYSTEM_PROMPT}]

for turn_num, user_msg in enumerate(LONG_CONVERSATION, 1):
    print(f"\n{'='*50}")
    print(f"Turn {turn_num} | Messages in context: {count_messages(messages_full)[0]} ({count_messages(messages_full)[1]} chars)")
    print(f"User: {user_msg}")
    messages_full.append({"role": "user", "content": user_msg})
    answer = tool_loop(messages_full)
    print(f"\nAssistant: {answer}")

msg_count, char_count = count_messages(messages_full)
print(f"\n--- Final stats: {msg_count} messages, ~{char_count} characters ---")

# %% [markdown]
# #### Approach B: Managed memory
# After every 3 user turns, compress older messages into a summary.
# We keep the last 3 turns in full.

# %%
print("=" * 60)
print("APPROACH B: Managed Memory (compress every 3 turns, keep last 3)")
print("=" * 60)

messages_managed = [{"role": "system", "content": SYSTEM_PROMPT}]

for turn_num, user_msg in enumerate(LONG_CONVERSATION, 1):
    # Compress every 3 turns
    if turn_num > 3 and (turn_num - 1) % 3 == 0:
        print(f"\n  *** COMPRESSING MEMORY ***")
        before = count_messages(messages_managed)
        messages_managed = compress_messages(messages_managed, keep_recent=3)
        after = count_messages(messages_managed)
        print(f"  Before: {before[0]} messages ({before[1]} chars)")
        print(f"  After:  {after[0]} messages ({after[1]} chars)")
        # Show the summary that was generated
        summary_msg = next((m for m in messages_managed if "Summary of earlier" in str(_get(m, "content", ""))), None)
        if summary_msg:
            print(f"  Summary: {summary_msg['content'][:200]}...")
        else:
            print(f"  (not enough turns to compress yet)")

    print(f"\n{'='*50}")
    print(f"Turn {turn_num} | Messages in context: {count_messages(messages_managed)[0]} ({count_messages(messages_managed)[1]} chars)")
    print(f"User: {user_msg}")
    messages_managed.append({"role": "user", "content": user_msg})
    answer = tool_loop(messages_managed)
    print(f"\nAssistant: {answer}")

msg_count, char_count = count_messages(messages_managed)
print(f"\n--- Final stats: {msg_count} messages, ~{char_count} characters ---")

# %% [markdown]
# #### Compare the results
#
# Look at the last two turns (7 and 8) — these are the memory tests:
# - Turn 7 asks "which of the **two spells I asked about first**..." (Vortexia and Glacius Torrent, from turns 1-2)
# - Turn 8 asks "remind me — what was the **potion I could brew with moonpetal**?" (from turn 3)
#
# **Questions to think about:**
# - Did Approach B answer turns 7 and 8 correctly? Did the summary preserve enough detail?
# - How much smaller was the message list in Approach B by the end?
# - What happens if you change `keep_recent` from 3 to 2? To 1? At what point does it break?
# - What if the summary prompt is less specific — does it lose important details?

# %% [markdown]
# ## 7. Interactive Chat
#
# Two versions for free-form testing. Type `quit` to exit.

# %%
def chat(use_memory=False, compress_every=4, keep_recent=3):
    """Interactive chat loop.

    Args:
        use_memory: if True, compress older turns into summaries
        compress_every: compress after this many turns
        keep_recent: keep this many recent turns in full after compression
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    turn_count = 0
    mode = "managed memory" if use_memory else "full history"
    print(f"Hogwarts Wizard Assistant — {mode} (type 'quit' to exit)")
    print("-" * 50)

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not user_input:
            continue

        turn_count += 1

        if use_memory and turn_count > compress_every and (turn_count - 1) % compress_every == 0:
            print("  [Compressing conversation memory...]")
            before = count_messages(messages)
            messages = compress_messages(messages, keep_recent=keep_recent)
            after = count_messages(messages)
            print(f"  [{before[0]} messages → {after[0]} messages]")

        messages.append({"role": "user", "content": user_input})
        answer = tool_loop(messages)
        msg_count, char_count = count_messages(messages)
        print(f"\nAssistant: {answer}")
        print(f"  [{msg_count} messages in context, ~{char_count} chars]")


# Uncomment one of these to run:
# chat(use_memory=False)   # Approach A: full history
# chat(use_memory=True)    # Approach B: managed memory

# %% [markdown]
# ## What to pay attention to
#
# Looking at the logs above, you should be able to answer:
#
# 1. **How does the model decide** whether to call a tool or just respond?
# 2. **What does the message list look like** after a multi-tool chain?
#    (system → user → assistant with tool_calls → tool result → ... → assistant text)
# 3. **Why does `tool_call_id` matter?** What would break if you didn't include it?
# 4. **Full history vs. managed memory** — what did each approach get right/wrong on
#    the recall questions (turns 7-8)? How much context did each use?
# 5. **The cost of memory** — summarization itself costs an API call. When is it
#    worth it? (Hint: think about conversations with 50+ turns)

# %%
