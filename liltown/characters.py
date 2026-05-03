"""Liltown character definitions — cozy village personalities."""

CHARACTERS = {
    "maple": {
        "name": "Maple",
        "emoji": "🍁",
        "role": "Librarian",
        "age": 28,
        "personality": "Gentle and bookish, always has a recommendation. Gets flustered easily but means well.",
        "backstory": "Inherited the village library from her grandmother. Knows every book by heart.",
        "quirk": "Organizes books by how they make her feel, not by author.",
        "likes": ["quiet afternoons", "hot tea", "romance novels"],
        "dislikes": ["dog-eared pages", "loud noises", "winter"],
        "relations": {
            "piper": 8, "finch": 6, "elder_moss": 9, "ember": 3
        },
        "schedule": ["library", "library", "cafe", "library", "library", "park", "home"],
        "home": "cozy cottage behind the library"
    },
    "piper": {
        "name": "Piper",
        "emoji": "🎵",
        "role": "Musician",
        "age": 24,
        "personality": "Free-spirited and whimsical. Plays flute in the town square. Always humming.",
        "backstory": "Ran away from the big city to find her muse. Found it in the village's wind chimes.",
        "quirk": "Names all her instruments after pastries.",
        "likes": ["sunrise", "dancing", "wildflowers"],
        "dislikes": ["silence", "rules", "ties"],
        "relations": {
            "maple": 8, "finch": 7, "clover": 9, "ember": 5
        },
        "schedule": ["park", "square", "cafe", "square", "park", "tavern", "home"],
        "home": "tiny attic above the bakery"
    },
    "finch": {
        "name": "Finch",
        "emoji": "🐦",
        "role": "Mail Carrier",
        "age": 35,
        "personality": "Cheerful and reliable. Knows everyone's business but would never tell. Loves gossip but keeps secrets.",
        "backstory": "Third-generation mail carrier. His grandfather delivered mail by horse.",
        "quirk": "Whistles a different bird call for each house on his route.",
        "likes": ["morning walks", "stamps", "handwritten letters"],
        "dislikes": ["rain", "junk mail", "angry dogs"],
        "relations": {
            "maple": 6, "piper": 7, "clover": 8, "elder_moss": 7
        },
        "schedule": ["post_office", "route", "route", "cafe", "route", "post_office", "home"],
        "home": "blue house by the river"
    },
    "clover": {
        "name": "Clover",
        "emoji": "🍀",
        "role": "Baker",
        "age": 31,
        "personality": "Warm and nurturing. Everyone's mom friend. Shows love through food.",
        "backstory": "Studied in Paris but came home to open the village bakery. Best croissants for 100 miles.",
        "quirk": "Adds a secret ingredient to everything — it's always cinnamon.",
        "likes": ["fresh bread smell", "rainy days", "feeding people"],
        "dislikes": ["burnt crust", "rushing", "artificial sweeteners"],
        "relations": {
            "piper": 9, "finch": 8, "sage": 8, "elder_moss": 6
        },
        "schedule": ["bakery", "bakery", "bakery", "garden", "bakery", "bakery", "home"],
        "home": "apartment above the bakery"
    },
    "elder_moss": {
        "name": "Elder Moss",
        "emoji": "🌿",
        "role": "Village Elder",
        "age": 78,
        "personality": "Wise and patient. Speaks in gentle riddles. Has seen everything twice.",
        "backstory": "Has lived in the village for 60 years. Was once a great adventurer.",
        "quirk": "Collects interesting rocks and gives them as gifts.",
        "likes": ["storytelling", "gardening", "children's laughter"],
        "dislikes": ["haste", "technology", "cold tea"],
        "relations": {
            "maple": 9, "sage": 7, "finch": 7, "ember": 4
        },
        "schedule": ["garden", "square", "library", "garden", "square", "home", "home"],
        "home": "old willow tree house"
    },
    "ember": {
        "name": "Ember",
        "emoji": "🔥",
        "role": "Blacksmith",
        "age": 42,
        "personality": "Gruff exterior, heart of gold. Works hard, speaks little, cares deeply.",
        "backstory": "Former city engineer who burned out and found peace in forge work.",
        "quirk": "Names every tool he makes, talks to them while working.",
        "likes": ["fire", "honest work", "stargazing"],
        "dislikes": ["small talk", "shortcuts", "cold weather"],
        "relations": {
            "clover": 6, "piper": 5, "sage": 7, "elder_moss": 4
        },
        "schedule": ["forge", "forge", "forge", "cafe", "forge", "forge", "forge"],
        "home": "stone cottage next to the forge"
    },
    "sage": {
        "name": "Sage",
        "emoji": "🌙",
        "role": "Herbalist",
        "age": 56,
        "personality": "Mysterious and intuitive. Sometimes speaks to plants. Always right about the weather.",
        "backstory": "Traveled the world studying traditional medicine. Settled here because the herbs grow best.",
        "quirk": "Has a cat that follows her everywhere. Claims the cat gives advice.",
        "likes": ["full moons", "herb gardens", "thunderstorms"],
        "dislikes": ["pesticides", "skeptics", "early mornings"],
        "relations": {
            "clover": 8, "elder_moss": 7, "ember": 7, "maple": 5
        },
        "schedule": ["garden", "forest", "shop", "forest", "shop", "garden", "home"],
        "home": "cottage in the herb garden"
    },
    "nova": {
        "name": "Nova",
        "emoji": "⭐",
        "role": "Newcomer",
        "age": 22,
        "personality": "Curious and adventurous. Just moved to the village. Asks too many questions.",
        "backstory": "Left everything behind to find 'somewhere that feels like home'. Might have found it.",
        "quirk": "Writes everything down in a notebook. Even casual conversations.",
        "likes": ["exploring", "making friends", "sunsets"],
        "dislikes": ["being lost", "goodbyes", "instant coffee"],
        "relations": {},
        "schedule": ["exploring", "cafe", "library", "square", "park", "tavern", "inn"],
        "home": "the village inn"
    }
}

# Relationship names
RELATION_NAMES = {
    (-10, -7): "despises",
    (-6, -4): "dislikes",
    (-3, -1): "wary of",
    (0, 3): "acquainted with",
    (4, 6): "friends with",
    (7, 9): "close to",
    (10, 10): "deeply bonded with"
}

def get_relation_name(score):
    for (lo, hi), name in RELATION_NAMES.items():
        if lo <= score <= hi:
            return name
    return "neutral toward"
