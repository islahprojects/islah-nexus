from pathlib import Path


HTML = Path("public_mirror/index.html")
ROOT_HTML = Path("index.html")


def read(path):
    return path.read_text(encoding="utf-8-sig").lower()


def test_public_mirror_exists():
    assert HTML.exists()


def test_public_mirror_is_warm_and_kind():
    text = read(HTML)

    assert "warm public mirror" in text
    assert "you are welcome here" in text
    assert "care first" in text
    assert "walang maiiwan" in text


def test_public_mirror_no_register_no_hidden_sync():
    text = read(HTML)

    assert "no register" in text
    assert "no account" in text
    assert "no hidden sync" in text
    assert "no hidden storage" in text


def test_public_mirror_blocks_overclaims():
    text = read(HTML)

    forbidden = [
        "agi complete",
        "production ready",
        "runtime sealed",
        "verified final",
        "perfect truth",
        "autonomous execution enabled",
    ]

    for phrase in forbidden:
        assert phrase not in text

    assert "no private keys" in text


def test_public_mirror_static_no_external_calls():
    text = read(HTML)

    assert "fetch(" not in text
    assert "xmlhttprequest" not in text
    assert "localstorage" not in text
    assert "sessionstorage" not in text
    assert "api." not in text


def test_public_mirror_has_no_gumroad_link():
    mirror_text = read(HTML)
    assert "gumroad" not in mirror_text

    if ROOT_HTML.exists():
        root_text = read(ROOT_HTML)
        assert "gumroad" not in root_text
