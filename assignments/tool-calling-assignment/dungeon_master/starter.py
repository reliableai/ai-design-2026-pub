# ============================================================
# Dungeon Master's Helper — Your Implementation
# ============================================================

import os
import json
import random
from dotenv import load_dotenv
from openai import OpenAI
from data import (
    CHARACTER, ITEMS,
    SYSTEM_PROMPT, STARTER_CONVERSATIONS,
)

load_dotenv()
client = OpenAI()
MODEL = "gpt-4.1-mini"
print(f"Client ready — using {MODEL}")


# ── 1. Tool functions (implement these) ─────────────────────

def roll_dice(sides: int, count: int) -> dict:
    """Roll `count` dice with `sides` sides each.

    Args:
        sides: number of sides per die (e.g. 20 for a d20)
        count: how many dice to roll

    Returns:
        dict with "rolls" (list of individual results) and "total"
    """
    # TODO: implement this
    # Example return: {"rolls": [14], "total": 14}
    pass


def lookup_item(name: str) -> dict:
    """Look up an item by name in the items table.

    Args:
        name: the item name (case-insensitive)

    Returns:
        dict with item stats, or {"error": "Item not found"} if missing
    """
    # TODO: implement this
    # Hint: use ITEMS dict, normalize the name to lowercase
    pass


def check_ability(character: str, skill: str) -> dict:
    """Check a character's ability modifier for a given skill.

    Args:
        character: character name (we only have one: "Lyra Shadowstep")
        skill: the skill to check (e.g. "stealth", "perception")

    Returns:
        dict with "character", "skill", "modifier" — or {"error": ...} if skill not found
    """
    # TODO: implement this
    # Hint: use CHARACTER dict
    pass


# ── 2. Tool schemas (write these) ───────────────────────────

# TODO: define the tool schemas for roll_dice, lookup_item, check_ability
#
# Format:
# {
#     "type": "function",
#     "function": {
#         "name": "...",
#         "description": "...",
#         "parameters": {
#             "type": "object",
#             "properties": { ... },
#             "required": [ ... ]
#         }
#     }
# }

TOOL_SCHEMAS = [
    # your schemas here
]

TOOLS = {
    "roll_dice": roll_dice,
    "lookup_item": lookup_item,
    "check_ability": check_ability,
}


# ── 3. Conversation loop ────────────────────────────────────

# TODO: implement TWO versions of the conversation loop.
#
# APPROACH A — Full history:
#   Send the entire message list every time. Simple and correct.
#   Build this first to get everything working.
#
#   The basic structure:
#   messages = [{"role": "system", "content": SYSTEM_PROMPT}]
#   while True:
#       user_input = input("You: ")
#       messages.append({"role": "user", "content": user_input})
#       # call the API with messages + tool schemas
#       # if response has tool_calls:
#       #     execute each tool, append results, call API again
#       # if response has text content:
#       #     print it, continue to next user input
#
# APPROACH B — Managed memory:
#   After every N turns, ask the LLM to summarize older messages.
#   Replace the old messages with the summary. Keep only the last
#   few turns in full. This saves tokens but may lose details.
#
# Remember to print the full message flow at each step!
# See README.md for the full spec.
# Test both approaches with the starter conversations AND the
# longer memory management conversation (test 5).
