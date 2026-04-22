# ============================================================
# Space Mission Planner — Your Implementation
# ============================================================

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from data import (
    PLANETS, SHIPS,
    SYSTEM_PROMPT, STARTER_CONVERSATIONS,
)

load_dotenv()
client = OpenAI()
MODEL = "gpt-4.1-mini"
print(f"Client ready — using {MODEL}")


# ── 1. Tool functions (implement these) ─────────────────────

def get_planet_info(planet: str) -> dict:
    """Look up information about a planet.

    Args:
        planet: planet name (case-insensitive)

    Returns:
        dict with planet data, or {"error": "Planet not found"} if unknown
    """
    # TODO: implement this
    pass


def calculate_travel_time(origin: str, destination: str, ship: str) -> dict:
    """Calculate travel time between two planets for a given ship.

    Uses simplified straight-line distance (difference in AU from sun).
    Real orbits are more complex, but this is good enough for our game.

    Args:
        origin: departure planet name
        destination: arrival planet name
        ship: ship name

    Returns:
        dict with distance_au, speed_au_per_day, travel_days, and fuel_needed,
        or {"error": ...} if planet or ship not found
    """
    # TODO: implement this
    # Steps:
    # 1. Look up both planets in PLANETS to get their distance_from_sun_au
    # 2. Calculate distance = abs(origin_au - destination_au)
    # 3. Look up the ship in SHIPS to get max_speed_au_per_day
    # 4. travel_days = distance / speed
    # 5. fuel_needed = distance * ship's fuel_consumption_per_au
    # 6. Return all the numbers
    pass


def check_fuel(ship: str, distance_au: float) -> dict:
    """Check if a ship has enough fuel for a given distance.

    Args:
        ship: ship name
        distance_au: distance to travel in AU

    Returns:
        dict with fuel_needed, fuel_capacity, enough_fuel (bool),
        and fuel_remaining if enough, or {"error": ...} if ship not found
    """
    # TODO: implement this
    pass


# ── 2. Tool schemas (write these) ───────────────────────────

# TODO: define the tool schemas for get_planet_info, calculate_travel_time, check_fuel
# Note: check_fuel takes a float parameter — make sure the schema type is "number"
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
    "get_planet_info": get_planet_info,
    "calculate_travel_time": calculate_travel_time,
    "check_fuel": check_fuel,
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
