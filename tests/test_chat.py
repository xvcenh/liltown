"""Tests for liltown chat engine."""

import pytest
from liltown.chat import ChatEngine
from liltown.characters import CHARACTERS


class TestChatEngine:
    def test_init_defaults(self):
        engine = ChatEngine()
        assert engine.day == 1
        assert engine.time == 8
        assert engine.api_key == ""

    def test_init_with_api_key(self):
        engine = ChatEngine(api_key="test-key", model="test-model")
        assert engine.api_key == "test-key"
        assert engine.model == "test-model"

    def test_advance_time_basic(self):
        engine = ChatEngine()
        engine.advance_time(3)
        assert engine.time == 11
        assert engine.day == 1

    def test_advance_time_overflow(self):
        engine = ChatEngine()
        engine.advance_time(20)
        assert engine.time == 4
        assert engine.day == 2

    def test_advance_time_multiple_days(self):
        engine = ChatEngine()
        engine.advance_time(48)
        assert engine.time == 8
        assert engine.day == 3

    def test_fallback_chat_returns_string(self):
        engine = ChatEngine()
        result = engine._fallback_chat("maple", "piper")
        assert isinstance(result, str)
        assert len(result) > 10

    def test_fallback_chat_includes_names(self):
        engine = ChatEngine()
        result = engine._fallback_chat("maple", "ember")
        assert "Maple" in result
        assert "Ember" in result

    def test_fallback_chat_has_variation(self):
        engine = ChatEngine()
        seen = set()
        for _ in range(15):
            seen.add(engine._fallback_chat("maple", "piper"))
        assert len(seen) >= 2  # At least 2 unique from 7 templates

    def test_fallback_chat_records_history(self):
        engine = ChatEngine()
        assert len(engine.history) == 0
        engine._fallback_chat("maple", "piper")
        assert len(engine.history) == 1
        assert engine.history[0]["char1"] == "maple"
        assert engine.history[0]["char2"] == "piper"

    def test_build_prompt_includes_context(self):
        engine = ChatEngine()
        prompt = engine._build_prompt("maple", "ember")
        assert "Maple" in prompt
        assert "Ember" in prompt
        assert "Librarian" in prompt
        assert "Blacksmith" in prompt
        assert "Day 1" in prompt

    def test_build_prompt_includes_relationship(self):
        engine = ChatEngine()
        # maple->ember has score 3
        prompt = engine._build_prompt("maple", "ember")
        assert "acquainted with" in prompt
        assert "(3/10)" in prompt
