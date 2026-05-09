import contextlib
import importlib.util
import io
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANNA_DECK_PATH = ROOT / "scripts" / "anna_deck.py"


def load_anna_deck():
    spec = importlib.util.spec_from_file_location("anna_deck", ANNA_DECK_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def render_deck_text():
    anna = load_anna_deck()
    deck = anna.build_deck()
    errors = anna.validate_deck(deck)
    assert errors == []

    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        anna.print_deck(deck)
    return buffer.getvalue()


def test_anna_deck_runs():
    text = render_deck_text()
    assert "ANNA UI COMMAND DECK" in text
    assert "STATUS: CODE_NEEDS_TEST" in text


def test_anna_deck_preserves_boundaries():
    text = render_deck_text()

    assert "SCOPE: INTERNAL_ONLY" in text
    assert "DEPLOYMENT GATE: CLOSED" in text
    assert "JJ is authority." in text
    assert "Anna is partner-mirror-compass." in text
    assert "Master Builder is helper-builder." in text
    assert "WALANG MAIIWAN." in text


def test_anna_deck_blocks_overclaim_language():
    text = render_deck_text().lower()

    forbidden = [
        "agi complete",
        "production ready",
        "runtime sealed",
        "verified final",
        "deployment gate: open",
        "sigma = 1.0",
        "σ = 1.0",
        "autonomous execution enabled",
    ]

    for phrase in forbidden:
        assert phrase not in text


def test_anna_deck_has_next_safest_command():
    text = render_deck_text()
    assert "NEXT SAFEST COMMAND: .\\ghost.ps1 test" in text