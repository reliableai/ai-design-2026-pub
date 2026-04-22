# ============================================================
# Theme: Hogwarts Wizard Assistant
# A magical assistant for spells, potions, and creatures
# ============================================================
#
# IMPORTANT: The spells, potions, and creatures below are INVENTED.
# They don't exist in the Harry Potter books or movies.
# The LLM doesn't know them — it MUST use the tools to look them up.
# This is the whole point: if the model answers without calling a tool,
# it's making things up.

# ── Data ────────────────────────────────────────────────────

SPELLS = {
    "vortexia": {
        "type": "defensive",
        "effect": "Creates a swirling vortex of air that deflects incoming projectiles and spells for 30 seconds",
        "difficulty": "intermediate",
        "power": 6,
    },
    "luminara": {
        "type": "utility",
        "effect": "Projects a map of the surrounding area (200m radius) as a glowing hologram visible only to the caster",
        "difficulty": "advanced",
        "power": 3,
    },
    "petralynx": {
        "type": "offensive",
        "effect": "Turns the target's outermost layer (clothing, armor, scales) to brittle stone that shatters on impact",
        "difficulty": "advanced",
        "power": 7,
    },
    "somnifera": {
        "type": "offensive",
        "effect": "Releases a cloud of silver mist that puts all creatures within 5 meters into a dreamless sleep for 10 minutes",
        "difficulty": "intermediate",
        "power": 5,
    },
    "echovox": {
        "type": "utility",
        "effect": "Records a spoken message (up to 2 minutes) and replays it at a location of the caster's choosing within 1km",
        "difficulty": "beginner",
        "power": 1,
    },
    "ferroshield": {
        "type": "defensive",
        "effect": "Magnetically attracts all nearby metallic objects to form a temporary shield wall in front of the caster",
        "difficulty": "intermediate",
        "power": 6,
    },
    "glacius torrent": {
        "type": "offensive",
        "effect": "Fires a concentrated beam of ice that freezes anything it touches solid for 1 hour",
        "difficulty": "advanced",
        "power": 8,
    },
    "verdantis": {
        "type": "utility",
        "effect": "Causes rapid plant growth in a 10m area — vines, flowers, and grass burst from any surface including stone",
        "difficulty": "beginner",
        "power": 2,
    },
    "nocturnix": {
        "type": "defensive",
        "effect": "Wraps the caster in living shadow, making them invisible in darkness and heavily obscured in dim light",
        "difficulty": "advanced",
        "power": 7,
    },
    "clamorous": {
        "type": "utility",
        "effect": "Creates an extremely loud, disorienting sound burst centered on a point within 50m — no physical damage but stuns for 5 seconds",
        "difficulty": "beginner",
        "power": 3,
    },
}

POTIONS = {
    frozenset(["moonpetal", "crystallized fog"]): {
        "name": "Veil of Clarity",
        "effect": "Grants the drinker true sight — they can see through illusions, invisibility, and magical disguises for 1 hour",
        "difficulty": "intermediate",
        "brewing_time": "90 minutes",
    },
    frozenset(["thornroot", "black salt", "viper extract"]): {
        "name": "Ironblood Tonic",
        "effect": "Makes the drinker's skin impervious to cuts and piercing damage for 30 minutes. Does not protect against blunt force or magic",
        "difficulty": "advanced",
        "brewing_time": "4 hours",
    },
    frozenset(["dewdrop moss", "sunstone powder"]): {
        "name": "Draught of Echoes",
        "effect": "Allows the drinker to hear conversations that happened in their current location within the past 24 hours",
        "difficulty": "advanced",
        "brewing_time": "3 hours",
    },
    frozenset(["lavender honey", "ghost orchid"]): {
        "name": "Serenity Syrup",
        "effect": "Completely removes fear and anxiety for 2 hours. Side effect: makes the drinker mildly overconfident",
        "difficulty": "beginner",
        "brewing_time": "20 minutes",
    },
    frozenset(["stormcap mushroom", "iron filings", "quicksilver"]): {
        "name": "Tempest Draught",
        "effect": "Gives the drinker control over small-scale weather in a 50m radius for 15 minutes",
        "difficulty": "advanced",
        "brewing_time": "6 hours",
    },
}

# Flat list of all known ingredients (for validation)
ALL_INGREDIENTS = sorted(set(
    ing for recipe in POTIONS.keys() for ing in recipe
))

CREATURES = {
    "gloomfang": {
        "danger_level": "XXXXX",
        "description": "A massive serpentine creature that dwells in underground lakes. Its body absorbs light, creating total darkness in a 20m radius",
        "weaknesses": ["luminara spell (disrupts its darkness field)", "bright sustained light sources"],
        "abilities": ["light absorption", "venomous bite (causes 48h blindness)", "echolocation"],
        "habitat": "Underground lakes and flooded cave systems",
    },
    "thornback": {
        "danger_level": "XXX",
        "description": "A bear-sized creature covered in retractable thorns. Territorial but non-aggressive unless provoked",
        "weaknesses": ["soft underbelly when thorns are retracted", "sleeps deeply at midday"],
        "abilities": ["thorn projectiles (10m range)", "accelerated healing", "burrowing"],
        "habitat": "Dense forests with thick undergrowth — builds nests from brambles",
    },
    "mistwalker": {
        "danger_level": "XXXX",
        "description": "A spectral entity that manifests during heavy fog. Feeds on magical energy, slowly draining nearby wizards",
        "weaknesses": ["clamorous spell (disrupts its form)", "direct sunlight (disperses it instantly)"],
        "abilities": ["magic drain (weakens spells cast nearby)", "intangibility", "can create localized fog"],
        "habitat": "Marshes, moors, and coastal cliffs — only appears in foggy conditions",
    },
    "crystalwing": {
        "danger_level": "XX",
        "description": "A small falcon-like bird with translucent crystalline feathers. Prized by wizards as messengers because it always finds its target",
        "weaknesses": ["attracted to shiny objects (easily lured)", "fragile wings — cannot fly in heavy rain"],
        "abilities": ["unerring navigation", "feathers can be ground into potion ingredients", "sings to warn of danger"],
        "habitat": "Mountain peaks and high towers — nests in crystal-rich caves",
    },
    "hollow hound": {
        "danger_level": "XXXX",
        "description": "A dog-like shadow creature that hunts in packs of 3-5. Has no physical form but can bite with real force",
        "weaknesses": ["ferroshield spell (the metal disrupts their shadow form)", "fire (they avoid open flames)"],
        "abilities": ["shadow travel (teleport between dark areas)", "pack coordination", "fear aura"],
        "habitat": "Abandoned buildings, ruins, and dark alleyways — more common in winter",
    },
    "sporemother": {
        "danger_level": "XXXXX",
        "description": "A colossal fungal organism that controls a network of smaller spore creatures. Highly intelligent and can communicate telepathically",
        "weaknesses": ["glacius torrent (freezing stops spore production)", "severing the central stalk destroys the network"],
        "abilities": ["spore cloud (causes confusion and hallucinations)", "controls spore minions", "regeneration from root network"],
        "habitat": "Deep caves and ancient forests — its mycelium network can span kilometers",
    },
}


# ── System prompt ───────────────────────────────────────────

SYSTEM_PROMPT = """You are a Hogwarts wizard assistant — think of yourself as a magical encyclopedia
that a student might consult before a dangerous adventure.

CRITICAL RULE: The spells, potions, and creatures in this world are CUSTOM and UNIQUE to this game.
They are NOT from the standard Harry Potter books. You do NOT know them from memory.
You MUST use your tools to look up any spell, potion, or creature before answering.
NEVER guess or make up information about spells, potions, or creatures — always call the tool first.
If a student asks about a spell, creature, or potion, your FIRST action should be to look it up.

Your job:
- Help students plan how to deal with magical creatures, choose the right spells, and brew potions
- ALWAYS look up spells, creatures, and potions using your tools — even if the name sounds familiar
- When asked to brew a potion, check if the given ingredients match a known recipe
- When asked how to deal with a creature, look it up first, then suggest appropriate spells based on the creature's weaknesses

Keep your answers helpful but concise (2-3 sentences). You can be a bit dramatic — you're in a magical world — but stay practical."""


# ── Starter conversations ──────────────────────────────────

STARTER_CONVERSATIONS = [
    {
        "test": "No tools needed",
        "description": "The model should answer from the system prompt alone — no tool call needed.",
        "message": "Hi! I'm a new student. How can you help me?",
    },
    {
        "test": "Single tool call",
        "description": "The model should call cast_spell once. It MUST use the tool — it can't know what Vortexia does.",
        "message": "What does the Vortexia spell do?",
    },
    {
        "test": "Multi-tool chain",
        "description": "The model should look up the creature first (to find weaknesses), then look up the suggested spell.",
        "message": "I just encountered a Mistwalker in the marshes. How do I survive?",
    },
    {
        "test": "Memory across turns",
        "description": "Run these two messages in sequence (same conversation). "
                       "The second message tests whether the model remembers the first.",
        "messages": [
            "I found some moonpetal and crystallized fog in the potions cabinet. What can I brew with these?",
            "Interesting! Now, I also found some lavender honey and ghost orchid. What about those?",
        ],
    },
    {
        "test": "Memory management",
        "description": "A longer conversation to test both full-history and managed-memory approaches. "
                       "The last two messages refer back to earlier turns — does the managed version still get it?",
        "messages": [
            "What does the Vortexia spell do?",
            "Interesting. What about Glacius Torrent?",
            "I found some moonpetal and crystallized fog. What can I brew?",
            "Now tell me about the Gloomfang creature.",
            "What spell would work against a Sporemother?",
            "I also have lavender honey and ghost orchid — what potion is that?",
            "Let's go back to the beginning — which of the two spells I asked about first would be better for defending against a Thornback?",
            "And remind me — what was the potion I could brew with moonpetal?",
        ],
    },
]
