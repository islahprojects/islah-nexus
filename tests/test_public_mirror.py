from pathlib import Path


HTML = Path("public_mirror/index.html")


def test_public_mirror_exists():
    assert HTML.exists()


def test_public_mirror_is_warm_and_kind():
    text = HTML.read_text(encoding="utf-8-sig").lower()

    assert "warm public mirror" in text
    assert "you are welcome here" in text
    assert "care first" in text
    assert "walang maiiwan" in text


def test_public_mirror_no_register_no_hidden_sync():
    text = HTML.read_text(encoding="utf-8-sig").lower()

    assert "no register" in text
    assert "no account" in text
    assert "no hidden sync" in text
    assert "no hidden storage" in text


def test_public_mirror_blocks_overclaims():
    text = HTML.read_text(encoding="utf-8-sig").lower()

    forbidden = [
        "agi complete",
        "production ready",
        "runtime sealed",
        "verified final",
        "perfect truth",
        "autonomous execution enabled",
        "private key",
    ]

    for phrase in forbidden:
        if phrase == "private key":
            assert "no private keys" in text
        else:
            assert phrase not in text


def test_public_mirror_static_no_external_calls():
    text = HTML.read_text(encoding="utf-8-sig").lower()

    assert "fetch(" not in text
    assert "xmlhttprequest" not in text
    assert "localstorage" not in text
    assert "sessionstorage" not in text
    assert "api." not in text
