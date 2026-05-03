"""Tests for liltown — terminal village."""

import pytest
from liltown.characters import CHARACTERS, get_relation_name
from liltown.chat import ChatEngine


def test_characters_loaded():
    assert len(CHARACTERS) == 8
    for cid, c in CHARACTERS.items():
        assert "name" in c
        assert "emoji" in c
        assert "role" in c
        assert "personality" in c
        assert "quirk" in c
        assert len(c["schedule"]) == 7  # 7 time slots


def test_character_relationships():
    maple = CHARACTERS["maple"]
    assert "piper" in maple["relations"]
    assert maple["relations"]["piper"] == 8


def test_get_relation_name():
    assert get_relation_name(10) == "deeply bonded with"
    assert get_relation_name(8) == "close to"
    assert get_relation_name(5) == "friends with"
    assert get_relation_name(0) == "acquainted with"
    assert get_relation_name(-1) == "wary of"
    assert get_relation_name(-5) == "dislikes"
    assert get_relation_name(-10) == "despises"


def test_chat_engine_init():
    engine = ChatEngine()
    assert engine.day == 1
    assert engine.time == 8
    assert not engine.api_key


def test_chat_engine_advance_time():
    engine = ChatEngine()
    engine.advance_time(5)
    assert engine.time == 13
    engine.advance_time(15)
    assert engine.time == 4
    assert engine.day == 2


def test_fallback_chat():
    engine = ChatEngine()
    result = engine._fallback_chat("maple", "piper")
    assert "Maple" in result
    assert "Piper" in result
    assert len(result) > 20


def test_build_prompt():
    engine = ChatEngine()
    prompt = engine._build_prompt("maple", "ember")
    assert "Maple" in prompt
    assert "Ember" in prompt
    assert "Librarian" in prompt
    assert "Blacksmith" in prompt


def test_fallback_chat_unique():
    engine = ChatEngine()
    results = set()
    for _ in range(10):
        results.add(engine._fallback_chat("maple", "piper"))
    # Should have variation (at least 2 unique from 7 templates)
    assert len(results) >= 2


def test_characters_have_unique_homes():
    homes = {c["home"] for c in CHARACTERS.values()}
    assert len(homes) == 8
