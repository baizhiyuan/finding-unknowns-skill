from catalog import load, search_key


def test_casefold():
    assert search_key("Straße") == "strasse"


def test_ascii_prefix():
    assert search_key("Apple").startswith("app")


def test_editions_remain_separate():
    assert len({(r["isbn"], r["edition"]) for r in load()}) == 4
