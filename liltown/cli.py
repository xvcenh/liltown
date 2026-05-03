"""Liltown CLI — run your cozy terminal village."""

import argparse
import os
import time
import threading
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from .village import VillageRenderer

console = Console()


def main():
    parser = argparse.ArgumentParser(
        prog="liltown",
        description="🏡 A cozy terminal village where AI characters live, chat, and build relationships"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="LLM API key (or set LLM_KEY env var)",
        default=os.environ.get("LLM_KEY", "")
    )
    parser.add_argument(
        "--endpoint", "-e",
        help="LLM API endpoint",
        default=os.environ.get("LLM_ENDPOINT", "https://api.deepseek.com/v1")
    )
    parser.add_argument(
        "--model", "-m",
        help="LLM model name",
        default=os.environ.get("LLM_MODEL", "deepseek-chat")
    )
    parser.add_argument(
        "--interval", "-i",
        type=float, default=5.0,
        help="Seconds between village ticks (default: 5)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Use pre-generated dialogue (no API calls)"
    )
    
    args = parser.parse_args()
    
    # Setup
    village = VillageRenderer()
    
    if args.quiet:
        village.chat.api_key = ""
    elif args.api_key:
        village.chat.api_key = args.api_key
        village.chat.api_endpoint = args.endpoint
        village.chat.model = args.model
    
    if not village.chat.api_key:
        console.print()
        console.print(Panel(
            "[yellow]💡 No API key provided. Using cozy pre-generated dialogue.[/yellow]\n"
            "[dim]Set LLM_KEY env var or use --api-key for AI-powered conversations.[/dim]\n"
            "[dim]Example: liltown --api-key sk-xxxxx[/dim]",
            title="Welcome to Liltown!",
            border_style="yellow"
        ))
        console.print()
    
    # Show startup
    village.add_event("🌅 The sun rises over Liltown. A new day begins.")
    
    # Run village loop
    stop_event = threading.Event()
    live = Live(village.render(), console=console, refresh_per_second=4, screen=True)
    
    try:
        with live:
            while not stop_event.is_set():
                time.sleep(args.interval)
                village.tick()
                live.update(village.render())
    except KeyboardInterrupt:
        console.print("\n[dim]👋 Goodbye from Liltown! The village will miss you.[/dim]")
