# ============================================================
# Theme: Space Mission Planner
# A mission control assistant for interplanetary travel
# ============================================================

# ── Data ────────────────────────────────────────────────────

PLANETS = {
    "mercury": {
        "distance_from_sun_au": 0.39,
        "diameter_km": 4879,
        "gravity_m_s2": 3.7,
        "atmosphere": "Virtually none — trace sodium and helium",
        "temperature_range": "-180°C to 430°C",
        "fun_fact": "A year on Mercury is just 88 Earth days, but a day lasts 59 Earth days.",
    },
    "venus": {
        "distance_from_sun_au": 0.72,
        "diameter_km": 12104,
        "gravity_m_s2": 8.87,
        "atmosphere": "Extremely thick CO2 — surface pressure 90x Earth",
        "temperature_range": "462°C average (hotter than Mercury despite being farther)",
        "fun_fact": "Venus rotates backwards compared to most planets.",
    },
    "earth": {
        "distance_from_sun_au": 1.0,
        "diameter_km": 12742,
        "gravity_m_s2": 9.81,
        "atmosphere": "Nitrogen-oxygen mix — the good stuff",
        "temperature_range": "-89°C to 57°C",
        "fun_fact": "The only known planet with pizza.",
    },
    "mars": {
        "distance_from_sun_au": 1.52,
        "diameter_km": 6779,
        "gravity_m_s2": 3.72,
        "atmosphere": "Thin CO2 — about 1% of Earth's pressure",
        "temperature_range": "-140°C to 20°C",
        "fun_fact": "Home to Olympus Mons, the tallest volcano in the solar system (21.9 km).",
    },
    "jupiter": {
        "distance_from_sun_au": 5.20,
        "diameter_km": 139820,
        "gravity_m_s2": 24.79,
        "atmosphere": "Hydrogen and helium — no solid surface",
        "temperature_range": "-145°C (cloud tops)",
        "fun_fact": "The Great Red Spot is a storm that has been raging for at least 350 years.",
    },
    "saturn": {
        "distance_from_sun_au": 9.58,
        "diameter_km": 116460,
        "gravity_m_s2": 10.44,
        "atmosphere": "Hydrogen and helium — less dense than water",
        "temperature_range": "-178°C (cloud tops)",
        "fun_fact": "Saturn's rings are mostly ice particles, some as small as grains of sand, others as big as houses.",
    },
    "neptune": {
        "distance_from_sun_au": 30.07,
        "diameter_km": 49528,
        "gravity_m_s2": 11.15,
        "atmosphere": "Hydrogen, helium, methane — the methane gives it its blue color",
        "temperature_range": "-214°C (cloud tops)",
        "fun_fact": "Winds on Neptune can reach 2,100 km/h — the fastest in the solar system.",
    },
}

SHIPS = {
    "aurora": {
        "type": "Explorer",
        "max_speed_au_per_day": 0.05,
        "fuel_capacity_units": 100,
        "fuel_consumption_per_au": 8,
        "crew_capacity": 6,
        "features": "Long-range scanners, geological survey lab",
    },
    "falcon": {
        "type": "Fast Courier",
        "max_speed_au_per_day": 0.12,
        "fuel_capacity_units": 60,
        "fuel_consumption_per_au": 12,
        "crew_capacity": 3,
        "features": "Speed-optimized engines, minimal cargo space",
    },
    "titan": {
        "type": "Heavy Freighter",
        "max_speed_au_per_day": 0.03,
        "fuel_capacity_units": 200,
        "fuel_consumption_per_au": 6,
        "crew_capacity": 12,
        "features": "Massive cargo bay, reinforced hull, slow but reliable",
    },
    "hermes": {
        "type": "Science Vessel",
        "max_speed_au_per_day": 0.08,
        "fuel_capacity_units": 120,
        "fuel_consumption_per_au": 10,
        "crew_capacity": 8,
        "features": "Full laboratory suite, atmospheric analysis equipment",
    },
}


# ── System prompt ───────────────────────────────────────────

SYSTEM_PROMPT = """You are a mission control assistant for an interplanetary space agency.

Your job:
- Help plan missions between planets: check distances, calculate travel times, verify fuel requirements
- Use your tools to get real data — don't estimate from memory
- When asked about a mission, look up the planets involved, calculate the travel time for the requested ship, and check if the ship has enough fuel
- If a mission isn't feasible, explain why and suggest alternatives

Keep answers concise and practical (2-3 sentences). You can have some fun with it — you're in space — but accuracy matters. Lives depend on your calculations."""


# ── Starter conversations ──────────────────────────────────

STARTER_CONVERSATIONS = [
    {
        "test": "No tools needed",
        "description": "The model should answer from the system prompt / general knowledge.",
        "message": "What kind of missions does this agency handle?",
    },
    {
        "test": "Single tool call",
        "description": "The model should call get_planet_info once.",
        "message": "Tell me about Mars. Could humans survive on the surface?",
    },
    {
        "test": "Multi-tool chain",
        "description": "The model should calculate travel time (which gives distance), then check fuel.",
        "message": "Can the Falcon make it from Earth to Jupiter?",
    },
    {
        "test": "Memory across turns",
        "description": "Run these two messages in sequence (same conversation). "
                       "The second tests whether the model remembers the first.",
        "messages": [
            "Plan a mission from Earth to Mars using the Aurora.",
            "What if we used the Titan instead? Would it be slower but safer on fuel?",
        ],
    },
    {
        "test": "Memory management",
        "description": "A longer conversation to test both full-history and managed-memory approaches. "
                       "The last two messages refer back to earlier turns.",
        "messages": [
            "Tell me about Mars.",
            "Can the Falcon make it from Earth to Mars?",
            "What about Jupiter — give me the planet info.",
            "Plan a trip from Earth to Jupiter with the Aurora.",
            "Is the Hermes faster than the Aurora?",
            "What about Neptune — how far is that?",
            "Going back to the start — remind me, could the Falcon reach Mars and how long would it take?",
            "And what was the fuel situation for the Aurora going to Jupiter?",
        ],
    },
]
