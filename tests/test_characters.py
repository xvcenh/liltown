"""Tests for liltown character system."""

import pytest
from liltown.characters import CHARACTERS, get_relation_name


class TestCharacters:
    def test_all_characters_loaded(self):
        assert len(CHARACTERS) == 8

    def test_character_has_required_fields(self):
        for cid, c in CHARACTERS.items():
            assert "name" in c, f"{cid} missing name"
            assert "emoji" in c, f"{cid} missing emoji"
            assert "role" in c, f"{cid} missing role"
            assert "personality" in c, f"{cid} missing personality"
            assert "quirk" in c, f"{cid} missing quirk"
            assert "schedule" in c, f"{cid} missing schedule"
            assert len(c["schedule"]) == 7, f"{cid} schedule should have 7 slots"

    def test_characters_have_unique_homes(self):
        homes = [c["home"] for c in CHARACTERS.values()]
        assert len(homes) == len(set(homes))

    def test_relations_maple(self):
        maple = CHARACTERS["maple"]
        assert maple["relations"]["piper"] == 8
        assert maple["relations"]["elder_moss"] == 9

    @pytest.mark.parametrize("score,expected", [
        (10, "deeply bonded with"),
        (8, "close to"),
        (5, "friends with"),
        (2, "acquainted with"),
        (0, "acquainted with"),
        (-2, "wary of"),
        (-5, "dislikes"),
        (-8, "despises"),
    ])
    def test_relation_names(self, score, expected):
        assert get_relation_name(score) == expected

    def test_nova_no_relations(self):
        nova = CHARACTERS["nova"]
        assert nova["relations"] == {}
