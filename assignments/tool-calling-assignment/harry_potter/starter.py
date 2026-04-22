# ============================================================
# Hogwarts Wizard Assistant — Your Implementation
# ============================================================

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from data import (
    SPELLS, POTIONS, ALL_INGREDIENTS, CREATURES,
    SYSTEM_PROMPT, STARTER_CONVERSATIONS,
)

load_dotenv()
client = OpenAI()
MODEL = "gpt-4.1-mini"
print(f"Client ready — using {MODEL}")


# ── 1. Tool functions (implement these) ─────────────────────

def cast_spell(spell_name: str) -> dict:
    """Look up a spell by name and return its details.

    Args:
        spell_name: name of the spell (case-insensitive)

    Returns:
        dict with spell info, or {"error": "Spell not found"} if unknown
    """
    # TODO: implement this
    # Hint: normalize spell_name to lowercase, look up in SPELLS dict
    pass


def brew_potion(ingredients: list) -> dict:
    """Check if a set of ingredients makes a known potion.

    Args:
        ingredients: list of ingredient names

    Returns:
        dict with potion info if valid combo, or
        {"error": "No known potion with these ingredients",
         "known_ingredients": ALL_INGREDIENTS} if no match
    """
    # TODO: implement this
    # Hint: convert ingredients list to frozenset, look up in POTIONS dict
    pass


def lookup_creature(name: str) -> dict:
    """Look up a magical creature by name.

    Args:
        name: creature name (case-insensitive)

    Returns:
        dict with creature info, or {"error": "Creature not found"} if unknown
    """
    # TODO: implement this
    # Hint: normalize name to lowercase, look up in CREATURES dict
    pass


# ── 2. Tool schemas (write these) ───────────────────────────

# TODO: define the tool schemas for cast_spell, brew_potion, lookup_creature
# Each schema tells the model what the tool does and what parameters it takes.
# Note: brew_potion takes an array parameter — check the OpenAI docs for
# how to define array types in JSON Schema.
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
    "cast_spell": cast_spell,
    "brew_potion": brew_potion,
    "lookup_creature": lookup_creature,
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
