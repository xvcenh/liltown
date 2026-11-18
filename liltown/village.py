"""Terminal village rendering — cozy ASCII art scene with Rich."""

import random
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
from .characters import CHARACTERS
from .chat import ChatEngine


class VillageRenderer:
    """Render the cozy terminal village with Rich."""

    def __init__(self):
        self.console = Console()
        self.chat = ChatEngine()
        self.log = []  # Recent events/chat
        self.weather = random.choice(["☀️ Sunny", "🌤️ Partly cloudy", "🌧️ Light rain", "🌈 Rainbow", "🌙 Starry night"])
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
        """Show newest entries first, treating model dialogue as literal text."""
        text = Text()
        if not self.log:
            return Text("The village is quiet... waiting for life to begin.", style="dim italic")
        for entry in reversed(self.log[-max_lines:]):
            if text:
                text.append("\n")
            text.append(f"Day {entry['day']} {entry['time']:02d}:00 ", style="dim")
            text.append(entry["text"])
        return text

    @property
    def season(self):
        seasons = ("Spring 🌸", "Summer 🌻", "Autumn 🍂", "Winter ❄️")
        return seasons[((self.chat.day - 1) // 7) % len(seasons)]

    def _weather_panel(self):
        return f"{self.weather}  |  Day {self.chat.day}  |  {self.season}"

    def render(self):
        """Build the full layout."""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=max(4, min(12, self.console.height // 3)))
        )
        
        compact = self.console.width < 78 or self.console.height < 21
        header_text = "🏡 Liltown" if compact else "🏡 Liltown — A Cozy Terminal Village"
        layout["header"].update(Panel(Align.center(Text(header_text, style="bold yellow")), border_style="yellow"))
        if compact:
            roster = Text(self._weather_panel() + "\n\n", style="italic cyan")
            for cid, character in CHARACTERS.items():
                is_active = cid in self.active_chars
                roster.append(character["name"] + "  ", style="bold cyan" if is_active else "white")
            layout["main"].update(Panel(roster, title="👥 Villagers", border_style="green"))
        else:
            layout["main"].split_row(Layout(name="scene", ratio=2), Layout(name="sidebar", ratio=1))
            art = Text(self._build_village_scene(), style="green")
            weather = Text(self._weather_panel(), style="italic cyan")
            layout["scene"].update(Panel(Text.assemble(art, "\n\n", weather), title="🌍 Village",
                                         border_style="green", padding=(0, 2)))
            roster = Text.from_markup(self._character_list())
            layout["sidebar"].update(Panel(roster, title="👥 Villagers", border_style="magenta"))

        # Footer — recent log
        log_text = self._recent_log()
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
