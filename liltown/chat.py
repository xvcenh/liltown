"""AI Chat engine — autonomous character conversations powered by LLM."""

import asyncio
import os
import random
from collections import deque
from .characters import CHARACTERS, get_relation_name


class ChatEngine:
    """Manages AI-powered conversations between villagers."""

    def __init__(self, api_endpoint=None, api_key=None, model=None):
        self.api_endpoint = api_endpoint or os.environ.get("LLM_ENDPOINT", "https://api.deepseek.com/v1")
        self.api_key = api_key or os.environ.get("LLM_KEY", "")
        self.model = model or os.environ.get("LLM_MODEL", "deepseek-chat")
        self.history = deque(maxlen=100)
        self.relations = {cid: dict(char.get("relations", {})) for cid, char in CHARACTERS.items()}
        self.day = 1
        self.time = 8  # 0-23

    def _build_prompt(self, char1_id, char2_id, context=""):
        c1 = CHARACTERS[char1_id]
        c2 = CHARACTERS[char2_id]
        
        rel_score = self.relations[char1_id].get(char2_id, 0)
        rel_name = get_relation_name(rel_score)
        
        prompt = f"""You are generating dialogue for a cozy terminal village game called Liltown.

## Current Scene
Time: {self.time}:00 | Day {self.day} | Season: Spring
Location: The village of Liltown — a peaceful, whimsical place

## Character 1: {c1['name']} {c1['emoji']}
Role: {c1['role']}
Personality: {c1['personality']}
Quirk: {c1['quirk']}
Current relationship with {c2['name']}: {rel_name} ({rel_score}/10)

## Character 2: {c2['name']} {c2['emoji']}
Role: {c2['role']}
Personality: {c2['personality']}
Quirk: {c2['quirk']}

{context}

## Task
Generate a short, cozy conversation between these two characters (4-6 lines total). 
Make it feel natural and warm — like Animal Crossing or Stardew Valley dialogue.
Show their personalities and relationship. Include small actions in *asterisks*.

Format:
{c1['name']}: [dialogue or *action*]
{c2['name']}: [dialogue or *action*]
...alternating...

Keep it brief and heartwarming. No conflict unless it fits their personalities. End with a natural fade-out."""
        
        return prompt

    async def generate_chat(self, char1_id, char2_id, context=""):
        """Use the same provider, timeout and offline fallback as the CLI."""
        return await asyncio.to_thread(self.generate_chat_sync, char1_id, char2_id, context)

    def _record(self, char1_id, char2_id, text):
        self.history.append({"char1": char1_id, "char2": char2_id, "text": text, "time": self.time})
        for source, target in ((char1_id, char2_id), (char2_id, char1_id)):
            self.relations[source][target] = min(10, self.relations[source].get(target, 0) + 1)
        return text

    def generate_chat_sync(self, char1_id, char2_id, context=""):
        """Synchronous version using requests."""
        if not self.api_key:
            return self._fallback_chat(char1_id, char2_id)

        prompt = self._build_prompt(char1_id, char2_id, context)
        
        messages = [
            {"role": "system", "content": "You are a dialogue generator for a cozy village game. Generate warm, natural conversations. Keep it short (4-6 lines)."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            import requests
            resp = requests.post(
                f"{self.api_endpoint}/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.9,
                    "max_tokens": 300
                },
                timeout=15
            )
            if resp.status_code == 200:
                data = resp.json()
                text = data["choices"][0]["message"]["content"]
                if isinstance(text, str) and text.strip():
                    return self._record(char1_id, char2_id, text)
        except Exception:
            pass
        
        return self._fallback_chat(char1_id, char2_id)

    def _fallback_chat(self, char1_id, char2_id):
        """Pre-generated cozy dialogue when no LLM is available."""
        c1 = CHARACTERS[char1_id]
        c2 = CHARACTERS[char2_id]
        
        templates = [
            f"{c1['name']}: *waves warmly* Good morning! How are you today?\n{c2['name']}: *smiles* Better now that I've seen you! The weather is perfect, isn't it?",
            f"{c1['name']}: I found the most wonderful thing today — want to see?\n{c2['name']}: *eyes light up* Oh, you know I can never resist your discoveries!",
            f"{c1['name']}: *humming softly* ...oh! I didn't see you there!\n{c2['name']}: *laughs* Don't stop on my account. That was lovely.",
            f"{c1['name']}: Would you like to share some tea? I just brewed a fresh pot.\n{c2['name']}: *sits down gratefully* You always know exactly what I need.",
            f"{c1['name']}: *holding a small gift* I thought of you when I saw this.\n{c2['name']}: *touched* You're too kind... truly. Thank you.",
            f"{c1['name']}: Have you seen the sunset from the hill lately?\n{c2['name']}: Not this week! Shall we go together tonight?",
            f"{c1['name']}: *reading quietly* ...oh! Hello there.\n{c2['name']}: What are you reading? Your face was so peaceful just now.",
        ]
        
        return self._record(char1_id, char2_id, random.choice(templates))

    def advance_time(self, hours=1):
        self.time += hours
        while self.time >= 24:
            self.time -= 24
            self.day += 1
