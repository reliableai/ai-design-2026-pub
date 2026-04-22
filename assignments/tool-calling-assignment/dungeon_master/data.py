# ============================================================
# Theme: Dungeon Master's Helper
# A tabletop RPG assistant that helps resolve player actions
# ============================================================

# ── Data ────────────────────────────────────────────────────

CHARACTER = {
    "name": "Lyra Shadowstep",
    "class": "Rogue",
    "level": 5,
    "hp": 38,
    "abilities": {
        "stealth": +5,
        "perception": +3,
        "lockpicking": +6,
        "acrobatics": +4,
        "persuasion": +1,
        "strength": -1,
        "arcana": +0,
    },
}

ITEMS = {
    "iron sword": {
        "type": "weapon",
        "damage": "1d8+2",
        "weight": 3,
        "properties": "Reliable but unremarkable.",
    },
    "elven dagger": {
        "type": "weapon",
        "damage": "1d4+3",
        "weight": 1,
        "properties": "Glows faintly near goblins. +1 to stealth attacks.",
    },
    "healing potion": {
        "type": "consumable",
        "effect": "Restores 2d4+2 HP",
        "weight": 0.5,
        "properties": "Tastes like warm honey. Single use.",
    },
    "rope of climbing": {
        "type": "gear",
        "effect": "50ft, can animate on command to anchor itself",
        "weight": 3,
        "properties": "Responds to the command word 'serpentis'.",
    },
    "golden amulet": {
        "type": "artifact",
        "effect": "Grants +2 to perception checks in dark places",
        "weight": 0.2,
        "properties": "Hums softly in the presence of magic. Origin unknown.",
    },
    "smoke bomb": {
        "type": "consumable",
        "effect": "Creates a 10ft cloud of smoke for 1 minute",
        "weight": 0.3,
        "properties": "Useful for quick escapes. 3 remaining.",
    },
    "thieves' tools": {
        "type": "gear",
        "effect": "Required for lockpicking attempts",
        "weight": 1,
        "properties": "A small leather pouch of picks, files, and pliers.",
    },
    "shield of echoes": {
        "type": "armor",
        "defense": "+2 AC",
        "weight": 6,
        "properties": "Emits a faint ringing sound when danger is within 30ft.",
    },
    "torch": {
        "type": "gear",
        "effect": "Illuminates 40ft radius for 1 hour",
        "weight": 1,
        "properties": "Standard adventuring torch.",
    },
    "mysterious map": {
        "type": "quest",
        "effect": "Shows a path to the Ruins of Valdris",
        "weight": 0,
        "properties": "The ink shifts when no one is looking. Partially illegible.",
    },
}


# ── System prompt ───────────────────────────────────────────

SYSTEM_PROMPT = """You are a Dungeon Master's helper for a tabletop RPG.

The player's character is Lyra Shadowstep, a Level 5 Rogue.

Your job:
- Help resolve player actions by checking abilities, rolling dice, and looking up items
- Narrate outcomes in a fun, immersive way (2-3 sentences, not novels)
- Use tools when the action requires a check, a roll, or item info
- Just talk normally for casual questions or roleplay that doesn't need mechanics

When resolving an action:
1. Check the relevant ability modifier
2. Roll the appropriate dice (usually d20 for checks)
3. Add the modifier to the roll. Total >= 12 is a success, < 12 is a failure
4. Narrate what happens

Keep it fun. You're a game master, not an accountant."""


# ── Starter conversations ──────────────────────────────────

STARTER_CONVERSATIONS = [
    {
        "test": "No tools needed",
        "description": "The model should answer from the system prompt alone.",
        "message": "What kind of character am I? What are my strengths?",
    },
    {
        "test": "Single tool call",
        "description": "The model should call lookup_item once.",
        "message": "What does my Elven Dagger do?",
    },
    {
        "test": "Multi-tool chain",
        "description": "The model should call check_ability then roll_dice, combine the results.",
        "message": "I try to sneak past the sleeping guard.",
    },
    {
        "test": "Memory across turns",
        "description": "Run these two messages in sequence (same conversation). "
                       "The second message tests whether the model remembers the first.",
        "messages": [
            "I pick up the golden amulet from the treasure chest and put it on.",
            "I enter a dark cave. Does my amulet help me here?",
        ],
    },
    {
        "test": "Memory management",
        "description": "A longer conversation to test both full-history and managed-memory approaches. "
                       "The last two messages refer back to earlier turns.",
        "messages": [
            "What does the Elven Dagger do?",
            "I try to sneak past a guard.",
            "I pick up the golden amulet and put it on.",
            "What's in my thieves' tools?",
            "I try to pick the lock on the iron gate.",
            "I throw a smoke bomb to cover my escape.",
            "Now that I'm safe — remind me, what bonus does the amulet give me?",
            "And what was the result of my lockpicking attempt earlier?",
        ],
    },
]
