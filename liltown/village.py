"""Terminal village rendering — cozy ASCII art scene with Rich."""

import random
import time
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
from rich.box import ROUNDED, SIMPLE
from .characters import CHARACTERS, RELATION_NAMES, get_relation_name
from .chat import ChatEngine


class VillageRenderer:
    """Render the cozy terminal village with Rich."""

    def __init__(self):
        self.console = Console()
        self.chat = ChatEngine()
        self.log = []  # Recent events/chat
        self.weather = random.choice(["☀️ Sunny", "🌤️ Partly cloudy", "🌧️ Light rain", "🌈 Rainbow", "🌙 Starry night"])
        self.season = "Spring 🌸"
        self.active_chars = []

    def _build_village_scene(self):
        """Build the ASCII art village scene."""
        lines = [
            "         🌙                              ☁️",
            "     🌲   ___     🏠       🌲",
            "    /🌳\\ |___|   ┌──┐     /🌲\\         🏠",
            "   /   \\  | |    │🏪│    /   \\        ┌──┐",
            "  🌲     ┌┴─┴┐  └──┘   🌳      🏠    │📚│   🌲",
            " /🌳\\    │🏠│          /🌲\\    ┌──┐   └──┘  /🌲\\",
            "/   \\  ┌┴──┴┐  🏠    /   \\   │☕│        /   \\",
            "│   │  │    │ ┌──┐  │   │  └──┘  🏠   │   │",
            "│   │  │    │ │🔨│  │   │        ┌──┐ │   │",
            "└───┘──┴────┴─┴──┴──┴───┴────────┴──┴─┴───┘",
            "    ~~~river~~~    🌿 garden    🌸 meadow",
        ]
        return "\n".join(lines)

    def _character_list(self):
        """Build a character status panel."""
        lines = []
        for cid, c in CHARACTERS.items():
            active = cid in self.active_chars
            marker = "●" if active else "○"
            style = "bold cyan" if active else "dim"
            lines.append(f"[{style}]{marker} {c['emoji']} {c['name']:<12}[/{style}] [dim]{c['role']}[/dim]")
        return "\n".join(lines)

    def _recent_log(self, max_lines=8):
        """Show recent events/chat."""
        if not self.log:
            return "[dim italic]The village is quiet... waiting for life to begin.[/dim italic]"
        
        lines = []
        for entry in self.log[-max_lines:]:
            lines.append(f"[dim]Day {entry['day']} {entry['time']:02d}:00[/dim] {entry['text']}")
        return "\n".join(lines)

    def _weather_panel(self):
        return f"{self.weather}  |  Day {self.chat.day}  |  {self.season}"

    def render(self):
        """Build the full layout."""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        
        layout["main"].split_row(
            Layout(name="scene", ratio=2),
            Layout(name="sidebar", ratio=1)
        )
        
        # Header
        header_text = Text("🏡 Liltown — A Cozy Terminal Village", style="bold yellow")
        layout["header"].update(Panel(Align.center(header_text), border_style="yellow"))
        
        # Village scene
        scene_text = Text(self._build_village_scene(), style="green")
        weather_text = Text(self._weather_panel(), style="italic cyan")
        scene_content = Text.assemble(scene_text, "\n\n", weather_text)
        layout["scene"].update(Panel(scene_content, title="🌍 Village", border_style="green", padding=(0, 2)))
        
        # Sidebar — character list
        char_text = Text.from_markup(self._character_list())
        layout["sidebar"].update(Panel(char_text, title="👥 Villagers", border_style="magenta"))
        
        # Footer — recent log
        log_text = Text.from_markup(self._recent_log())
        layout["footer"].update(Panel(log_text, title="💬 Recent Happenings", border_style="cyan"))
        
        return layout

    def add_event(self, text, char_id=None, char2_id=None):
        """Add an event to the log."""
        entry = {"text": text, "time": self.chat.time, "day": self.chat.day}
        self.log.append(entry)
        if char_id:
            self.active_chars.append(char_id)
        if char2_id:
            self.active_chars.append(char2_id)
        
        # Trim log
        if len(self.log) > 100:
            self.log = self.log[-100:]

    def tick(self):
        """Advance time and trigger events."""
        self.chat.advance_time()
        self.active_chars = []
        
        # Random weather changes
        if random.random() < 0.1:
            self.weather = random.choice([
                "☀️ Sunny", "🌤️ Partly cloudy", "🌧️ Light rain", 
                "🌈 Rainbow", "🌙 Starry night", "⛅ Overcast",
                "🌤️ Breezy", "🌸 Cherry blossom breeze"
            ])
        
        # Random character encounters
        chars = list(CHARACTERS.keys())
        if random.random() < 0.4:
            c1, c2 = random.sample(chars, 2)
            context = ""
            text = self.chat.generate_chat_sync(c1, c2, context)
            self.add_event(text, c1, c2)
        
        # Occasional solo activity
        if random.random() < 0.3:
            c = random.choice(chars)
            solo_actions = [
                f"{CHARACTERS[c]['emoji']} {CHARACTERS[c]['name']} is {random.choice(['reading quietly', 'tending the garden', 'writing a letter', 'humming a tune', 'watching the clouds', 'baking something sweet', 'feeding the birds', 'stargazing', 'sipping tea', 'practicing a new skill'])}.",
            ]
            self.add_event(random.choice(solo_actions), c)
