"""
This module contains the character tests.
"""
import character

def test_character_heal_full_health():
    """
    Test healing a character to full health.
    """
    game = None
    player = character.Character(game, 'Test Player', 'Test Description', health=2, attack_power=1)
    player.health = 1
    player.heal(player.max_health)
    assert player.health == player.max_health
